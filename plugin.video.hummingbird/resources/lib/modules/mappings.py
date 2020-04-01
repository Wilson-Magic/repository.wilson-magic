import requests
import json
import re

class Mappings:
    def __init__(self):
        #Trakt Stuff
        self.client_id = 'a15ae82439a6b3e2f8dabdf4b2ce1aade6b870262fa5af51233c0ba959d87004'
        self.client_secret = 'dd3ac49c29516a0c11daadc4c5b8b9a69b17dfd5a1a40d7f7f79fe0af00cd6f6'
        self.trakt_link = 'https://api.trakt.tv'
        self.trakt_headers = {'Content-type': 'application/json', 
                        'trakt-api-key': self.client_id,
                        'trakt-api-version': '2'}
        self.search_query = '/search/%s?query=%s'
        self.search_trakt = '/search/trakt/%s?id_type=%s'
        
        #Kitsu Stuff
        self.kitsu_link = 'https://kitsu.io/api/edge/anime/%s/mappings'
        self.kitsu_headers = {
            'Accept': 'application/vnd.api+json',
            'Content-Type': 'application/vnd.api+json'
            }
            
        #Other Stuff
        self.arm = 'https://hato.malupdaterosx.moe/api/mappings/%s/anime/%s'
        self.jikan = 'https://api.jikan.moe/v3/%s/%s'
        self.trakt_titles = {}
        
        self.mal_link = 'https://myanimelist.net'
        
        #Mappings
        self.kitsu = None
        self.mal = None
        self.anilist = None
        self.anidb = None
        self.trakt = None
        self.tvdb = None
        self.tmdb = None
        self.imdb = None

    def get(self, kitsu_id, type, year):
        try: self.getKitsu(kitsu_id)
        except: pass
        try: self.getArm(kitsu_id)  #Modifying this to make it better
        except: pass
        try: self.getTraktTitle()
        except: pass
        try: self.getTrakt(type, year)
        except: pass

        mappings = {
            'kitsu': self.kitsu,
            'mal': self.mal,
            'anilist': self.anilist,
            'anidb': self.anidb,
            'trakt': self.trakt,
            'tvdb': self.tvdb,
            'tmdb': self.tmdb,
            'imdb': self.imdb
            }        
            
        return mappings
        
    def getKitsu(self, id):
        self.kitsu = id
        
        resp = requests.get('https://kitsu.io/api/edge/anime/%s/mappings' % self.kitsu, headers=self.kitsu_headers)
        load = json.loads(resp.content)
        
        data = load['data']
        
        for a in data:
            attr = a['attributes']
            if attr['externalSite'] == 'anidb':
                self.anidb = attr['externalId']
            if attr['externalSite'] == 'anilist':
                self.anilist = attr['externalId'].replace('anime/', '')
            if attr['externalSite'] == 'myanimelist/anime':
                self.mal = attr['externalId']
            if attr['externalSite'] == 'trakt':
                self.trakt = attr['externalId']
        
    def getArm(self, id):
        try:
            resp = requests.get('https://arm.now.sh/api/v1/search?type=%s&id=%s' % (site, id))
            load = json.loads(resp.content)
            self.anilist = load['services']['anilist']
            self.anidb =  load['services']['anidb']
            self.mal =  load['services']['mal']
        except:
            #Try Hato then Notify then just take the data
            resp = requests.get('https://hato.malupdaterosx.moe/api/mappings/%s/anime/%s' % (site, id), headers={'User-Agent': tools.get_random_ua()})
            load = json.loads(resp.content)
            data = load['data']
            try:
                notify = data['notify_id']
                resp = requests.get('https://notify.moe/api/anime/%s' % notify)
                load = json.loads(resp.content)
                mappings = load['mappings']
                for a in mappings:
                    if a['service'] == 'anilist/anime':
                        self.anilist = a['serviceId']
                    if a['service'] == 'myanimelist/anime':
                        self.mal = a['serviceId']
                    if a['service'] == 'anidb/anime':
                        self.anidb = a['serviceId']
                    if a['service'] == 'trakt/anime':
                        self.trakt = a['serviceId']
            except:
                self.anidb = data['anidb_id']
                self.anilist = data['anilist_id']
                self.mal = data['mal_id']
        
        
    def getTraktTitle(self):
        resp = requests.get(self.mal_link + '/anime/%s' % self.mal)
        load = str(resp.content)
        
        base_anime_title = re.findall(r'og:title" content="(.*?)"', load)[0]
        eng_anime_title = next(iter(re.findall(r'English:</span> (.*?)\\', load)), None)
        
        adaption = re.findall(r'Adaptation:</td>(.*?)<tr>', load)[0]
        manga_link = re.findall(r'<a href="(.*?)"', adaption)[0]

        resp = requests.get(self.mal_link + manga_link)
        load = str(resp.content)
        
        base_manga_title = re.findall(r'og:title" content="(.*?)"', load)[0]
        eng_manga_title = next(iter(re.findall(r'English:</span> (.*?)<', load)), None)
        
        self.trakt_titles = {
            'anime': {
                'base': base_anime_title,
                'english': eng_anime_title
                },
            'manga': {
                'base': base_manga_title,
                'english': eng_manga_title
                }
            }
        
    def getTrakt(self, type, year):
        if type == 'movie':
            id_type = 'movie'
        else:
            id_type = 'show'
            
        if self.trakt != None:
            resp = requests.get(self.trakt_link + self.search_trakt % (self.trakt, id_type), headers=self.trakt_headers)
            load = json.loads(resp.content)
        else:
            if self.trakt_titles['manga']['english'] != None: 
                resp = requests.get(self.trakt_link + self.search_query % (id_type, self.trakt_titles['manga']['english']), headers=self.trakt_headers)
            else: 
                resp = requests.get(self.trakt_link + self.search_query % (id_type, self.trakt_titles['anime']['english']), headers=self.trakt_headers)
            load = json.loads(resp.content)       

        correct_trakt_item = ''

        for a in load:
            if self.trakt:
                if id_type != 'movie':
                    if a['type'] == id_type:
                        correct_trakt_item = a
                else:
                    if a['type'] == id_type and str(a[id_type]['year']) == year:
                        correct_trakt_item = a
            else:
                if id_type != 'movie':
                    try:
                        if a[id_type]['title'] == self.trakt_titles['anime']['base']:
                            correct_trakt_item = a
                        if a[id_type]['title'] == self.trakt_titles['anime']['english']:
                            correct_trakt_item = a
                        if a[id_type]['title'] == self.trakt_titles['manga']['base']:
                            correct_trakt_item = a
                        if a[id_type]['title'] == self.trakt_titles['manga']['english']:
                            correct_trakt_item = a
                    except:
                        continue
                else:
                    try:
                        if a[id_type]['title'] == self.trakt_titles['anime']['base'] and str(a[id_type]['year']) == year:
                            correct_trakt_item = a
                        if a[id_type]['title'] == self.trakt_titles['anime']['english'] and str(a[id_type]['year']) == year:
                            correct_trakt_item = a
                        if a[id_type]['title'] == self.trakt_titles['manga']['base'] and str(a[id_type]['year']) == year:
                            correct_trakt_item = a
                        if a[id_type]['title'] == self.trakt_titles['manga']['english'] and str(a[id_type]['year']) == year:
                            correct_trakt_item = a
                    except:
                        continue
        
        ids = correct_trakt_item[id_type]['ids']
        
        self.trakt = ids['trakt']
        try: self.tvdb = ids['tvdb']  #Have to put a try except here as tvdb doesn't do movies
        except: self.tvdb = None
        self.tmdb = ids['tmdb']
        self.imdb = ids['imdb']
