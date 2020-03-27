# -*- coding: UTF-8 -*-

import providers
from resources.lib.modules import tools
from resources.lib.modules.worker import ThreadPool
import time


class NectarScraper:
    def __init__(self):
        # Base Variables
        self.hosters = providers.get_hosters()
        self.torrents = providers.get_torrents()
        self.remaining_providers = []
        self.sources = {}
        self.data = {}
        self.task_queue = ThreadPool()

        # Scraping Strings
        self.heading = tools.addonName + ': Scraping'
        self.startingLineOne = 'Starting Scraping...'
        self.hosterLineOne = 'Hosters Scraping...'
        self.torrentLineOne = 'Torrents Scraping...'
        self.episodeLineOne = 'Scraping %s - Episode %s'
        self.movieLineOne = 'Scraping %s'
        self.LineTwo = 'Remaining Providers: %s'
        self.LineThree = 'Sources Found: %s'

        # Pre-emptive Settings
        self.preemp_minimum_sources = int(tools.getSetting('preemptive.limit'))
        self.preemp_resolution = int(tools.getSetting('preemptive.resolution'))
        self.preemptive_source_type = tools.getSetting('preemptive.sourcetype')
        self.preemptive_audiotype = tools.getSetting('preemptive.audiotype')

    def scrape(self, data):
        tools.progressDialog.create(heading=self.heading, line1=self.startingLineOne)
        self.data = data

        if 'episode' in self.data:
            tools.progressDialog.update(0, line1=self.episodeLineOne % (
                self.data['titles']['canon'], self.data['episode']))
        else:
            tools.progressDialog.update(0, line1=self.movieLineOne % self.data['titles']['canon'])

        for provider in self.torrents:
            if tools.getSetting(provider) == 'true':
                self.remaining_providers.append(provider)
                self.task_queue.put(self._scrape_torrent_provider, provider)

        for provider in self.hosters:
            if tools.getSetting(provider) == 'true':
                self.remaining_providers.append(provider)
                self.task_queue.put(self._scrape_hoster_provider, provider)

        run_time = 0
        max_time = int(tools.getSetting('scraping.timeout'))
        start_time = time.time()

        while len(self.remaining_providers) > 0 and not tools.progressDialog.iscanceled() and run_time < max_time:
            tools.progressDialog.update(self._get_progress_percentage(start_time),
                                        line2=self.LineTwo % self._get_provider_display_string(),
                                        line3=self.LineThree % len(self.sources))
            run_time += int(time.time() - start_time)
            time.sleep(1)

            # Check to see if we should break early if preemptive is on
            if tools.getSetting('preemptive.enable') == 'true':
                if self._check_preemptive():
                    break

        tools.progressDialog.close()

        if tools.getSetting('general.enablememes') == 'true':
            self._run_memes()

        self.sources = [value for key, value in self.sources.items()]

        return self.sources

    def _check_preemptive(self):

        try:
            selected_sources = [value for key, value in self.sources.items()]

            if self.preemptive_source_type == 'torrent':
                selected_sources += [i for i in selected_sources if i.get('source_type') == 'torrent']
            elif self.preemptive_source_type == 'hoster':
                selected_sources += [i for i in selected_sources if i.get('source_type') == 'hoster']

            if self.preemptive_audiotype != 'Any':
                selected_sources = [i for i in selected_sources if i.get('audio_type') == self.preemptive_audiotype]

            selected_sources = [i for i in selected_sources if i['quality'] >= self.preemp_resolution]

            if len(selected_sources) >= self.preemp_minimum_sources:
                return True
            else:
                return False
        except:
            import traceback
            traceback.print_exc()
            return False


    def _run_memes(self):
        # Memes
        memeLine1 = "Adding Wilson's Special Sauce ( ͡° ͜ʖ ͡°)"
        memeElipsis = ''
        memeProgress = 0

        tools.progressDialog.create(heading=self.heading, line1=memeLine1, line2=memeLine1, line3=memeLine1)
        for a in range(20):
            memeElipsis = memeElipsis + '.'
            tools.progressDialog.update(memeProgress, line1=memeLine1 + memeElipsis, line2=memeLine1 + memeElipsis,
                                        line3=memeLine1 + memeElipsis)
            memeProgress += 5
            if len(memeElipsis) == 3:
                memeElipsis = ''
            time.sleep(0.1)
        tools.progressDialog.close()

    def _get_provider_display_string(self):
        return ', '.join([i.upper() for i in self.remaining_providers])

    def _get_progress_percentage(self, start_time):
        return int(float(time.time()) - int(start_time))

    def _remove_provider(self, provider_name):
        try:
            self.remaining_providers.remove(provider_name)
        except:
            pass

    def _scrape_torrent_provider(self, provider_name):

        try:
            i = __import__('providers.torrents.%s' % provider_name, fromlist=['sub'], globals=globals())
            mod = i.source()
            if 'episode' in self.data:
                link = mod.tvshow(self.data)
            else:
                link = mod.movie(self.data)

            source = mod.sources(link)

            self._store_and_de_dup_sources(source, 'torrent')
        except Exception as e:
            tools.log('Error with %s:/n%s' % (provider_name, e), 'error')
        finally:
            self._remove_provider(provider_name)

    def _scrape_hoster_provider(self, provider_name):
        try:
            i = __import__('providers.hosters.%s' % provider_name, fromlist=['sub'], globals=globals())
            mod = i.source()

            if 'episode' in self.data:
                results = mod.tvshow(self.data)
            else:
                results = mod.movie(self.data)

            source = mod.sources(results)

            self._store_and_de_dup_sources(source, 'hoster')
        except Exception as e:
            tools.log('Error with %s:/n%s' % (provider_name, e), 'error')
        finally:
            self._remove_provider(provider_name)

    def _store_and_de_dup_sources(self, sources, type):
        if type == 'hoster':
            for source in sources:
                source['source_type'] = 'hoster'
                self.sources[source['link']] = source
        else:
            for source in sources:
                source['source_type'] = 'torrent'
                self.sources[source['hash']] = source