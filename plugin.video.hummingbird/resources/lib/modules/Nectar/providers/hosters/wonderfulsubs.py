import requests
import traceback

from resources.lib.modules import tools
from resources.lib.modules import crunchy_api


class WonderfulSession(requests.Session):

    def __init__(self):
        self._base_link = 'https://www.wonderfulsubs.com'
        super(WonderfulSession, self).__init__()

    def get(self, url, **kwargs):
        url = self._base_link + url
        return super(WonderfulSession, self).get(url, **kwargs)

    def post(self, url, **kwargs):
        url = self._base_link + url
        return super(WonderfulSession, self).post(url, **kwargs)

    def set_token(self, token):
        self.headers.update({'authorization': 'Bearer {}'.format(token)})


class source:
    def __init__(self):
        self.api_search = '/api/v2/media/search?options=summary&q=%s'
        self.api_series = '/api/v2/media/series?series={}'
        self.api_source = '/api/v2/media/stream?code%s%s'
        self._login_url = '/api/v2/users/login'

        self.source_dict = {
            'ka': 'KissAnime',
            'cr': 'Crunchyroll',
            'fa': 'Funimation'
        }
        self._user_name = tools.getSetting('ws.username')
        self._password = tools.getSetting('ws.password')
        self._session = WonderfulSession()
        if not self._user_name == '' or not self._password == '':
            self._try_set_token()
        self._is_authorized = False

    def _do_login(self):
        resp = self._session.post(self._login_url, json={'username': self._user_name, 'password': self._password}).json()
        return resp['token']

    def _try_set_token(self):
        token = tools.getSetting('ws.token')
        if token == '':
            token = self._do_login()

        self._session.set_token(token)
        tools.setSetting('ws.token', token)
        self._is_authorized = True

    def tvshow(self, data):
        #Get crunchy data
        try:
            crunchy_links = tools.get_kitsu_streaming_links(data['id'])
            crunchy_link = crunchy_links['crunchyroll']
            crunchy_titles = crunchy_api.CrunchyrollAPI().search(crunchy_link)
        except:
            crunchy_titles = []
    
        info = self._session.get(self.api_search % data['titles']['canon']).json()['json']
        series = info['series']
        shows = [a['url'] for a in series]
        sources = []

        for a in shows:
            try:
                id = a.replace('/watch/', '')
                info = self._session.get(self.api_series.format(id)).json()['json']
                kitsu_ids = info['kitsu_ids']
                anime = []
                anime_found = any(str(data['id']) == str(b) for b in kitsu_ids)
                episodes = {}
                if anime_found:
                    seasons = info['seasons']['ws']['media']
                    try:
                        episodes = []
                        for b in seasons:
                            try:
                                try:
                                    if str(b['kitsu_id']) == str(data['id']):
                                        episodes.append(b)
                                except:
                                    for c in crunchy_titles:
                                        if b['title'] == c:
                                            episodes.append(b)
                            except:
                                continue                        
                    except IndexError:
                        continue
                if len(episodes) == 0:
                    continue
                try:
                    for b in episodes:
                        for c in b['episodes']:
                            if int(c['episode_number']) == int(data['episode']):
                                try:
                                    sources.append(c['sources'])
                                except:
                                    sub = 'subs'
                                    if c['is_dubbed'] == True:
                                        sub = 'dubs'
                                    srcs = [{'source': 'cr',
                                            'language': sub,
                                            'retrieve_url': c['retrieve_url']}]
                                    sources.append(srcs)
                    break
                except IndexError:
                    continue
            except:
                traceback.print_exc()
                continue
        return sources

    def movie(self, data):
        # Movies do not work correctly on wonderfulsubs right now. pls fix red :P
        return

    def sources(self, data):
        source_list = []
        
        for a in data:
            for b in a:

                site = 'WonderfulSubs'
                try:
                    provider = self.source_dict[b['source']]
                    
                except KeyError:
                    continue

                audio = b['language'][:3].title()
                
                retrieve = b['retrieve_url']
                
                if type(retrieve) is list:
                    retrieve = b['retrieve_url'][0]
                    

                url = '/api/v2/media/stream?code={}&platform=Kodi'.format(tools.quote(retrieve))
                

                try:
                    urls = self._session.get(url).json()
                    
                    urls = urls['urls']
                    
                except KeyError:
                    continue
                except ValueError:
                    continue

                if not urls:
                    continue
                

                for c in urls:
                    try:
                        quality = ''
                        adaptive = False

                        if c['label'] == '360p':
                            quality = 360
                            
                        elif c['label'] == '480p':
                            quality = 480
                            
                        elif c['label'] == '720p':
                            quality = 720
                            
                        elif c['label'] == '1080p':
                            quality = 1080
                            
                        elif c['label'] == 'Auto (DASH)':
                            quality = 1080
                            adaptive = 'mpd'
                            
                        elif c['label'] == 'Auto (HLS)':
                            quality = 1080
                            adaptive = 'hls'
                            
                        elif c['label'] == 'HD':
                            quality = 720
                            

                        subtitles = c.get('captions', {}).get('src')
                        
                        source_dict = {
                            'site': site,
                            'source': provider,
                            'link': c.get('src', c.get('file')),
                            'quality': quality,
                            'audio_type': audio,
                            'adaptive': adaptive,
                            'subtitles': subtitles
                        }
                        
                        if source_dict['link'] is None:
                            continue
                            
                        source_list.append(source_dict)
                        
                    except KeyError:
                        traceback.print_exc()
                        continue
                        
        return source_list
