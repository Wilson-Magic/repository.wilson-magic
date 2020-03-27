import requests
import json

from resources.lib.modules import tools

class FanartTV:
    def __init__(self):
        self.base_url = 'http://webservice.fanart.tv/v3/%s/%s'
        self.api_key = 'dfe6380e34f49f9b2b9518184922b49c'
        self.client_key = tools.getSetting('key.fanart')
        self.lang = tools.getSetting('fanart.lang')
        self.languages = ['en', 'ja', '00', '']
        self.headers = {'client-key': self.client_key, 'api-key': self.api_key}
        
        self.art = {}
        
        self.season = ''
        
    def get(self, mappings, type, lang, season=None):
        #Ignore Lang it's just there to react differently when language is changed
        
        self.season = season
        
        query = ''
        link_query = ''
        fa_id = ''
        
        if season != None:
            query='season'
            link_query = 'tv'
            fa_id = mappings['tvdb']
        else:
            query = 'movies'
            link_query = 'movies'
            fa_id = mappings['tmdb']
        
        resp = requests.get(self.base_url % (link_query, fa_id), headers=self.headers)
        load = json.loads(resp.content)
        
        if query == 'movies':
            self.art.update(self.movieFanart(load, 'clearlogo', ['movielogo', 'hdmovielogo']))
            self.art.update(self.movieFanart(load, 'discart', ['moviedisc']))
            self.art.update(self.movieFanart(load, 'clearart', ['movieart', 'hdmovieclearart']))
            self.art.update(self.movieFanart(load, 'characterart', ['characterart']))
            self.art.update(self.movieFanart(load, 'poster', ['movieposter']))
            self.art.update(self.movieFanart(load, 'fanart', ['moviebackground']))
            self.art.update(self.movieFanart(load, 'banner', ['moviebanner']))
            self.art.update(self.movieFanart(load, 'landscape', ['moviethumb']))
            
        elif query == 'season':
            self.art.update(self.seasonFanart(load, 'clearlogo', ['hdtvlogo', 'clearlogo'], ['hdtvlogo', 'clearlogo']))
            self.art.update(self.seasonFanart(load, 'clearart', ['hdclearart', 'clearart'], ['hdclearart', 'clearart']))
            self.art.update(self.seasonFanart(load, 'characterart', ['characterart'], ['characterart']))
            self.art.update(self.seasonFanart(load, 'keyart', ['tvposter-alt'], ['tvposter-alt']))
            self.art.update(self.seasonFanart(load, 'landscape', ['seasonthumb'], ['tvthumb']))
            self.art.update(self.seasonFanart(load, 'banner', ['seasonbanner'], ['tvbanner']))
            self.art.update(self.seasonFanart(load, 'poster', ['seasonposter'], ['tvposter']))
            self.art.update(self.seasonFanart(load, 'fanart', ['showbackground-season'], ['showbackground'])) 

        return self.art            
                            
    def movieFanart(self, movie, name, types):
        art = {}
        
        art_list = []
        lang_list = []
        
        for a in movie:
            for b in types:
                if a == b:
                    if isinstance(movie[a], list):
                        for c in movie[a]:
                            art_list.append(c)
                    else:    
                        art_list.append(movie[a])
        
        for a in art_list:
            for b in self.languages:
                if a['lang'] == b:
                    lang_list.append(a)
                    
        lang_sort = ''
        if self.lang == 'English':
            lang_sort = 'en'
        else:
            lang_sort = 'ja'
        
        sorted_list = sorted(lang_list, key=lambda x: (x['lang']==lang_sort, int(x['likes'])), reverse=True)

        if len(sorted_list) > 0:
            art[name] = sorted_list[0]['url']
        
        return art
        
    def seasonFanart(self, show, name, season_types, tv_types):
        art={}
        
        art_list = []
        lang_list = []
        
        season_sort = False
        
        for a in show:
            for b in season_types:
                if a == b:
                    if name == 'landscape' or name == 'banner' or name == 'poster' or name == 'fanart':
                        season_sort = True
                        if isinstance(show[a], list):
                            for c in show[a]:
                                if str(c['season']) == str(self.season) or str(c['season']) == 'all':
                                    art_list.append(c)
                        else:
                            if str(a['season']) == str(self.season) or str(a['season']) == 'all':
                                art_list.append(show[a])
                    else:
                        if isinstance(show[a], list):
                            for c in show[a]:
                                art_list.append(c)
                        else:
                            art_list.append(show[a])
                        
        if len(art_list) == 0:
            season_sort = False
            for a in show:
                for b in tv_types:
                    if a == b:
                        if isinstance(show[a], list):
                            for c in show[a]:
                                art_list.append(c)
                        else:
                            art_list.append(show[a])
        
        for a in art_list:
            for b in self.languages:
                if a['lang'] == b:
                    lang_list.append(a)
                    
        lang_sort = ''
        if self.lang == 'English':
            lang_sort = 'en'
        else:
            lang_sort = 'ja'
        
        if season_sort == True:
            sorted_list = sorted(lang_list, key=lambda x: (x['season']!='all', x['lang']==lang_sort, int(x['likes'])), reverse=True)
        else:
            sorted_list = sorted(lang_list, key=lambda x: (x['lang']==lang_sort, int(x['likes'])), reverse=True)

        if len(sorted_list) > 0:
            art[name] = sorted_list[0]['url']
        
        return art                    