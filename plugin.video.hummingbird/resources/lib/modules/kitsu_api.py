import requests
import json
import math
import time
import re

from bs4 import BeautifulSoup

from resources.lib.modules import tools
from resources.lib.modules import mappings
from resources.lib.modules import cache
from resources.lib.modules.worker import ThreadPool

class Backend:
    def __init__(self):
        self.api_path = 'https://kitsu.io/api/edge'
        self.oauth_path = 'https://kitsu.io/api/oauth'
        
        self.client_id = 'dd031b32d2f56c990b1425efe6c42ad847e7fe3ab46bf1299f05ecd856bdb7dd'
        self.client_secret = '54d7307928f63414defd96399fc31ba847961ceaecef3a5fd93144e960c0e151'
        
        self.headers = {
            'Accept': 'application/vnd.api+json',
            'Content-Type': 'application/vnd.api+json'
            }
            
        if tools.getSetting('kitsu.access') is not '' and tools.getSetting('kitsu.18plus') is not 'false':
            self.headers['Authorization'] = 'Bearer %s' % tools.getSetting('kitsu.access')
        
    def request(self, url, page=1, limit=20, data=None):
        offset = (page-1)*limit
        add_url = 'page[limit]=%s&page[offset]=%s' % (limit, offset)
        if '?' in url:
            request_url = self.api_path + url + '&' + add_url
        else:
            request_url = self.api_path + url + '?' + add_url
        
        if data is None:
            response = requests.get(request_url, headers=self.headers)
        else:
            response = requests.post(request_url, headers=self.headers, data=data)       
        
        response = self.check_response(response)
        if response['status'] != 'OK':
            tools.showDialog.notification(tools.addonName, 'Kitsu Error: Check log for details')
            tools.log('Kitsu Error: %s - %s' % (response['code'], response['description']), 'error') 
            return

        return response['content']

    def check_response(self, response):
        response_dict = {}
        
        if response.status_code == 200:
            response_dict['code'] = response.status_code
            response_dict['status'] = 'OK'
            response_dict['description'] = 'OK - request succeeded (GET, PATCH, DELETE)'
            response_dict['content'] = response.content
        elif response.status_code == 201:
            response_dict['code'] = response.status_code
            response_dict['status'] = 'OK'
            response_dict['description'] = 'Created - new resource created (POST)'
            response_dict['content'] = response.content
        elif response.status_code == 204:
            response_dict['code'] = response.status_code
            response_dict['status'] = 'OK'
            response_dict['description'] = 'No Content - request succeeded (DELETE)'
            response_dict['content'] = response.content
        elif response.status_code == 400:
            response_dict['code'] = response.status_code
            response_dict['status'] = 'BAD'
            response_dict['description'] = 'Bad Request - malformed request'
            response_dict['content'] = response.content
        elif response.status_code == 401:
            response_dict['code'] = response.status_code
            response_dict['status'] = 'BAD'
            response_dict['description'] = 'Unauthorized - invalid or no authentication details provided'
            response_dict['content'] = response.content
        elif response.status_code == 404:
            response_dict['code'] = response.status_code
            response_dict['status'] = 'BAD'
            response_dict['description'] = 'Not Found - resource does not exist'
            response_dict['content'] = response.content
        elif response.status_code == 406:
            response_dict['code'] = response.status_code
            response_dict['status'] = 'BAD'
            response_dict['description'] = 'Not Acceptable - invalid Accept header'
            response_dict['content'] = response.content
        elif response.status_code >= 500:
            response_dict['code'] = response.status_code
            response_dict['status'] = 'BAD'
            response_dict['description'] = 'Server Error'
            response_dict['content'] = response.content
        else:
            response_dict['code'] = None
            response_dict['status'] = 'BAD'
            response_dict['description'] = 'No request'
            response_dict['content'] = None
            
        return response_dict
        
class KitsuBrowser:
    def __init__(self):
        self.thread_list = ThreadPool()
        self.remaining_threads = []
        self.episodeList = []
        self.extractedItems = []

    def trending(self):
        anime = []
        resp = cache.hummingCache().cacheCheck(Backend().request, 24, '/trending/anime')
        load = json.loads(resp)
        data = load['data']

        for a in data:
            self.remaining_threads.append(a['attributes']['canonicalTitle'])
            self.thread_list.put(self.extract, a)
            
        while len(self.remaining_threads) > 0:
            time.sleep(1)
        
        sortedItems = tools.sort_anime_by_json(self.extractedItems, data)
        
        return sortedItems
    
    def top_airing(self, page):
        anime = []
        
        sort_status = tools.getSetting('airing.sort')
        sort = tools.menu_sort[sort_status]
        
        resp = cache.hummingCache().cacheCheck(Backend().request, 24, '/anime?filter[status]=current&sort=%s' % (sort), page=page)
        load = json.loads(resp)
        data = load['data']

        for a in data:
            self.remaining_threads.append(a['attributes']['canonicalTitle'])
            self.thread_list.put(self.extract, a)
            
        while len(self.remaining_threads) > 0:
            time.sleep(1)
            
        sortedItems = tools.sort_anime_by_json(self.extractedItems, data)
        
        return sortedItems
        
    def top_upcoming(self, page):
        anime = []
        
        sort_status = tools.getSetting('upcoming.sort')
        sort = tools.menu_sort[sort_status]        
        
        resp = cache.hummingCache().cacheCheck(Backend().request, 24, '/anime?filter[status]=upcoming&sort=%s' % sort, page=page)
        load = json.loads(resp)
        data = load['data']
        
        for a in data:
            self.remaining_threads.append(a['attributes']['canonicalTitle'])
            self.thread_list.put(self.extract, a)
            
        while len(self.remaining_threads) > 0:
            time.sleep(1)
            
        sortedItems = tools.sort_anime_by_json(self.extractedItems, data)
        
        return sortedItems
        
    def most_popular(self, page):
        anime = []
        resp = cache.hummingCache().cacheCheck(Backend().request, 24, '/anime?sort=popularityRank', page=page)
        load = json.loads(resp)
        data = load['data']

        for a in data:
            self.remaining_threads.append(a['attributes']['canonicalTitle'])
            self.thread_list.put(self.extract, a)
            
        while len(self.remaining_threads) > 0:
            time.sleep(1)
            
        sortedItems = tools.sort_anime_by_json(self.extractedItems, data)
        
        return sortedItems
        
    def highest_rated(self, page):
        anime = []
        resp = cache.hummingCache().cacheCheck(Backend().request, 24, '/anime?sort=ratingRank', page=page)
        load = json.loads(resp)
        data = load['data']

        for a in data:
            self.remaining_threads.append(a['attributes']['canonicalTitle'])
            self.thread_list.put(self.extract, a)
            
        while len(self.remaining_threads) > 0:
            time.sleep(1)
            
        sortedItems = tools.sort_anime_by_json(self.extractedItems, data)
        
        return sortedItems
    
    def search(self, title=None, year=None, rating=None, season=None, subtype=None, genre=None, page=1):
        filters = []

        if title != None and title != '':
            filters.append('filter[text]=%s' % title)        
        if season == None or season == '':
            if year != None and year != '':
                filters.append('filter[season]=winter,spring,summer,fall&filter[seasonYear]=%s' % year)
        if season != None and season != '':
            if year == None or year == '':
                filters.append('filter[season]=%s' % season)     
            if year != None and year != '':        
                filters.append('filter[season]=%s&filter[seasonYear]=%s' % (season, year))
        if rating != None and rating != '':
            filters.append('filter[ageRating]=%s' % rating)
        if subtype != None and subtype != '':
            filters.append('filter[subtype]=%s' % subtype)
        if genre != None and genre != '':
            filters.append('filter[categories]=%s' % genre)
                
        #for a in filters:
            #if a == 'filter[text]=None':
                #filters.remove(a)

        filter_string = '&'.join(filters)

        sort_status = tools.getSetting('search.sort')
        sort_string = tools.menu_sort[sort_status]
        
        if title == None or title == '':
            request = '/anime?' + filter_string + '&sort=%s' % sort_string
        else:
            request = '/anime?' + filter_string
        
        anime = []
        
        resp = cache.hummingCache().cacheCheck(Backend().request, 24, request, page=page)
        load = json.loads(resp)
        data = load['data']

        for a in data:
            self.remaining_threads.append(a['attributes']['canonicalTitle'])
            self.thread_list.put(self.extract, a)
            
        while len(self.remaining_threads) > 0:
            time.sleep(1)
            
        sortedItems = tools.sort_anime_by_json(self.extractedItems, data)
        
        return sortedItems
                  
    
    def all_categories(self):
        categories = []
        resp = cache.hummingCache().cacheCheck(Backend().request, 24*7, '/categories', limit=217)
        load = json.loads(resp)
        data = load['data']
        
        for a in data:
            attributes = a['attributes']
            categories.append({'name': attributes['title'], 'description': attributes['description'], 'slug': attributes['slug'], 'child_count': attributes['childCount']})
            
        return categories
        
    def episodes(self, id, page):
        resp = cache.hummingCache().cacheCheck(Backend().request, 24, '/anime/%s/episodes' % id, page=page)
        load = json.loads(resp)
        data = load['data']
        
        for a in data:
            attributes = a['attributes']
            episode = {}
            
            try: episode['episode_title'] = attributes['canonicalTitle']
            except: episode['episode_title'] = None
            episode['alt_titles'] = {}
            try: episode['alt_titles']['romaji'] = attributes['titles']['en_jp']
            except: episode['alt_titles']['romaji'] = None
            try: episode['alt_titles']['kanji'] = attributes['titles']['ja_jp']
            except: episode['alt_titles']['kanji'] = None
            try:
                episode['alt_titles']['english'] = attributes['titles']['en']
            except:
                try: episode['alt_titles']['english'] = attributes['titles']['en_us']
                except: episode['alt_titles']['english'] = None
            
            try: episode['seasonNumber'] = attributes['seasonNumber']
            except: episode['seasonNumber'] = None
            try: episode['episodeNumber'] = attributes['number']
            except: episode['episodeNumber'] = None
            try: episode['relativeNumber'] = attributes['relativeNumber']
            except: episode['relativeNumber'] = None
            try: episode['episodePlot'] = attributes['synopsis']
            except: episode['episodePlot'] = None
            try: episode['year'] = attributes['airdate'][:4]
            except: episode['year'] = None
            try: episode['airdate'] = attributes['airdate']
            except: episode['airdate'] = None
            episode['episodeLength'] = attributes['length']
            try: episode['thumbnail'] = attributes['thumbnail']['original']
            except: episode['thumbnail'] = None
            
            self.episodeList.append(episode)
        
        self.remaining_threads.remove(page)
    
    def all_episodes(self, id):
        resp = cache.hummingCache().cacheCheck(Backend().request, 24, '/anime/%s/episodes' % id, page=1)       
        load = json.loads(resp)
        count = load['meta']['count']
        
        pages = int(math.ceil(float(int(count))/20))
        
        for a in range(pages):
            self.remaining_threads.append(a+1)
            self.thread_list.put(self.episodes, id, a+1)
        
        while len(self.remaining_threads) > 0:
            time.sleep(1)
        
        sortedEps = sorted(self.episodeList, key=lambda x: int(x['episodeNumber']), reverse=False)
        
        return sortedEps
        
    def getShow(self, id):
        resp = cache.hummingCache().cacheCheck(Backend().request, 24, '/anime/%s' % id)
        load = json.loads(resp)
        data = load['data']
     
        self.remaining_threads.append(data['attributes']['canonicalTitle'])
        self.thread_list.put(self.extract, data)
            
        while len(self.remaining_threads) > 0:
            time.sleep(1)
            
        show = self.extractedItems[0]
        
        return show
        
    def getListById(self, list, progress=None):
        items = []
        
        for a in list:
            resp = cache.hummingCache().cacheCheck(Backend().request, 24, '/anime/%s' % a)
            data = json.loads(resp)
            data = data['data']
            items.append(data)
            
        if progress != None:
            items[0]['account_info'] = progress

        tools.log(items)

        extracted_items = self.extract_items(items)

        return extracted_items        
        
    def getListbyLink(self, list):
        installments = []
        
        for a in list:
            resp = cache.hummingCache().cacheCheck(Backend().request, 24, a)
            load = json.loads(resp)
            data = load['data']
            installments.append(data)

        extracted_items = self.extract_items(installments)
        
        return extracted_items        
      
    def extract_items(self, list):
        for a in list:
            self.remaining_threads.append(a['attributes']['canonicalTitle'])
            self.thread_list.put(self.extract, a)
            
        while len(self.remaining_threads) > 0:
            time.sleep(1)

        return self.extractedItems
        
    def extract(self, item, progress=None):
        dict = {}
        attributes = item['attributes']
        
        dict['id'] = item['id']
        
        dict['titles'] = {}
        try: dict['titles']['canon'] = attributes['canonicalTitle']
        except: dict['titles']['canon'] = None
        try:
            dict['titles']['english'] = attributes['titles']['en']
        except:
            try:
                dict['titles']['english'] = attributes['titles']['en_us']
            except:
                dict['titles']['english'] = None
        try: dict['titles']['romaji'] = attributes['titles']['en_jp']
        except: dict['titles']['romaji'] = None
        try: dict['titles']['kanji'] = attributes['titles']['ja_jp']
        except: dict['titles']['kanji'] = None
        try: dict['abbreviated_titles'] = attributes['abbreviatedTitles']
        except: dict['abbreviated_titles'] = None
        
        year = ''
        
        try: 
            year = attributes['startDate'][:4]
        except:
            try:
                year = attributes['tba']        
            except:
                year = 0000
        
        dict['mappings'] = cache.hummingCache().cacheCheck(mappings.Mappings().get, 24, dict['id'], attributes['subtype'], year)
        
        try: dict['mal_titles'] = cache.hummingCache().cacheCheck(Other().getMALTitles, 24, dict['mappings'])
        except: dict['mal_titles'] = {}
        
        try: dict['plot'] = attributes['synopsis']
        except: sict['plot'] = None
        try: dict['year'] = attributes['startDate'][:4]
        except: dict['year'] = None
        try: dict['start_date'] = attributes['startDate']
        except: dict['start_date'] = None
        try: dict['end_date'] = attributes['endDate']
        except: dict['end_date'] = None
        try: dict['popularity_rank'] = attributes['popularityRank']
        except: dict['popularity_rank'] = None
        try: dict['rating_rank'] = attributes['ratingRank']
        except: dict['rating_rank'] = None
        try: dict['average_rating'] = attributes['averageRating']
        except: dict['average_rating'] = None
        try: dict['age_rating'] = attributes['ageRating']
        except: dict['age_rating'] = None
        try: dict['age_guide'] = attributes['ageRatingGuide']
        except: dict['age_guide'] = None
        try: dict['subtype'] = attributes['subtype']
        except: dict['subtype'] = None
        try: dict['status'] = attributes['status']
        except: dict['status'] = None
        try: dict['episode_count'] = attributes['episodeCount']
        except: dict['episode_count'] = None
        try: dict['episode_length'] = attributes['episodeLength']
        except: dict['episode_length'] = None
        try: dict['youtube_trailer'] = attributes['youtubeVideoId']
        except: dict['youtube_trailer'] = None
        try: dict['nsfw'] = attributes['nsfw']
        except: dict['nsfw'] = None
        
        try: dict['genres'] = Other().get_genres(item['id'])
        except: dict['genres'] = []
        
        try: dict['franchise_name'] = tools.get_franchise_name(dict['titles'])
        except: dict['franchise_name'] = None
        
        try: dict['season'] = tools.get_season_number(dict['titles'])
        except: dict['season'] = 1            
            
        qualities = ['original', 'large', 'medium', 'small', 'tiny']
        
        posterCheck = attributes['posterImage']
        fanartCheck = attributes['coverImage']
        
        poster = ''
        fanart = ''

        if posterCheck is not None:
            for a in qualities:
                if poster == '':
                    try: poster = posterCheck[a]
                    except: poster = ''
        if fanartCheck is not None:
            for a in qualities:
                if fanart == '':
                    try: fanart = fanartCheck[a]
                    except: fanart = ''

        dict['art'] = {}
        
        if not tools.getSetting('key.fanart') == '' and tools.getSetting('art.fanart') == 'true':
            from resources.lib.modules import fanarttv
                
            if dict['subtype'] == 'movie':
                try:
                    dict['art'] = cache.hummingCache().cacheCheck(fanarttv.FanartTV().get, 24, dict['mappings'], dict['subtype'], tools.getSetting('fanart.lang'))
                except:
                    pass
            else:
                try:
                    dict['art'] = cache.hummingCache().cacheCheck(fanarttv.FanartTV().get, 24, dict['mappings'], dict['subtype'], tools.getSetting('fanart.lang'), season=dict['season'])            
                except:
                    pass
            
            dict['art']['poster'] = dict['art'].get('poster', poster)
            dict['art']['fanart'] = dict['art'].get('fanart', fanart)
        else:
            try: dict['art']['poster'] = poster
            except: dict['art']['poster'] = None
            try: dict['art']['fanart'] = fanart
            except: dict['art']['fanart'] = None   

        try: dict['account_info'] = item['account_info']
        except: dict['account_info'] = None        
        
        self.remaining_threads.remove(item['attributes']['canonicalTitle'])  
        self.extractedItems.append(dict)

    def franchise(self, id):
        link = '/anime/%s/installments' % id
        resp = cache.hummingCache().cacheCheck(Backend().request, 24*7, link)
        load = json.loads(resp)
        
        installment_id = []
        franchise_id = []
        franchise_installments = []
        
        data = load['data']
        for a in data:
            installment_id.append(a['id'])
            
        for a in installment_id:
            link = '/installments/%s/franchise' % a
            resp = cache.hummingCache().cacheCheck(Backend().request, 24*7, link)
            load = json.loads(resp)
            data = load['data']
            franchise_id.append(data['id'])

        for a in franchise_id:
            link = '/franchises/%s/installments' % a 
            resp = cache.hummingCache().cacheCheck(Backend().request, 24*7, link)
            load = json.loads(resp)
            data = load['data']
            for b in data:
                franchise_installments.append('/installments/%s/media' % b['id'])
                
        anime = self.getListbyLink(franchise_installments)
                   
        return anime

class Other:
    def getMALTitles(self, mappings):
        resp = requests.get('https://myanimelist.net/anime/%s' % mappings['mal'])
        load = str(resp.content)
        
        titles = {}
        
        titles['base'] = re.findall(r'og:title" content="(.*?)"', load)[0]
        titles['english'] = next(iter(re.findall(r'English:</span> (.*?)\\', load)), None)
        titles['japanese'] = next(iter(re.findall(r'Japanese:</span> (.*?)\\', load)), None)
        
        return titles
        
  
    def get_genres(self, id):
        genre_list = []
        resp = cache.hummingCache().cacheCheck(Backend().request, 24*7, '/anime/%s/categories' % id, limit=217)
        load = json.loads(resp)
        data = load['data']
        
        for a in data:
            attributes = a['attributes']
            genre_list.append(attributes['title'])
            
        return genre_list
        
    def get_franchise(self, id):
        resp = cache.hummingCache().cacheCheck(Backend().request, 24*7, '/anime/%s/installments' % id)        
        load = json.loads(resp)
        data = load['data']
        
        franchise_link = data[0]['relationships']['franchise']['links']['related']
        franchise_link = franchise_link.replace('https://kitsu.io/api/edge', '')
        
        resp = cache.hummingCache().cacheCheck(Backend().request, 24*7, franchise_link)
        load = json.loads(resp)
        data = load['data']
        
        franchise = {}
        
        attributes = data['attributes']
        
        try: franchise['id'] = data['id']
        except: franchise['id'] = None
        franchise['titles'] = {}
        try: franchise['titles']['canon'] = attributes['canonicalTitle']
        except: franchise['titles']['canon'] = None
        try: franchise['titles']['english'] = attributes['titles']['en']
        except: franchise['titles']['english'] = None
        try: franchise['titles']['romaji'] = attributes['titles']['en_jp']
        except: franchise['titles']['romaji'] = None
        franchise['year'] = ''
        
        #This part is bullshit but its for mappings, takes a few requests LOL
        if franchise['id'] != None:        
            resp = cache.hummingCache().cacheCheck(Backend().request, 24, '/franchises/%s/installments' % franchise['id'])
            load = json.loads(resp)
            data = load['data']
            
            current_start_year = 1000000
            
            for a in data:
                link = a['relationships']['media']['links']['related']
                link = link.replace('https://kitsu.io/api/edge', '')

                resp = cache.hummingCache().cacheCheck(Backend().request, 24*7, link)
                load = json.loads(resp)
                media = load['data']
                
                year = int(media['attributes']['startDate'][:4])
                
                if year < current_start_year:
                    current_start_year = year

            franchise['year'] = current_start_year

        else:
            franchise['year'] = None
        
        return franchise
        
class Mappings:
    def __init__(self):
        #Anime Sites
        self.kitsu = ''
        self.mal = ''
        self.anilist = ''
        self.anidb = ''
        #Other Sites
        self.trakt = ''
        self.tvdb = ''
        self.tmdb = ''
        self.imdb = ''
        
        #Trakt Info
        self.client_id = 'a15ae82439a6b3e2f8dabdf4b2ce1aade6b870262fa5af51233c0ba959d87004'
        self.client_secret = 'dd3ac49c29516a0c11daadc4c5b8b9a69b17dfd5a1a40d7f7f79fe0af00cd6f6'
        self.api_path = 'https://api.trakt.tv'
        self.headers = {'Content-type': 'application/json', 
                        'trakt-api-key': self.client_id,
                        'trakt-api-version': '2'}
        self.search_movie = '/search/movie?query=%s'
        self.search_tv = '/search/show?query=%s'
        self.search_trakt = '/search/trakt/%s?id_type=%s'
        
    def get(self, data, type, year):
        
        self.kitsu = data['id']
        self.getKitsu(data['id'])
        
        #Check Based on Known Info
        if self.trakt == '':
            self.getTraktFromTitle(data['titles'], type, year)
        else:
            self.getTrakt(self.trakt, type, data['titles'])
            
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
        resp = cache.hummingCache().cacheCheck(Backend().request, 24, '/anime/%s/mappings' % id)
        load = json.loads(resp)
        data = load['data']
        for a in data:
            attributes = a['attributes']
            if attributes['externalSite'] == 'anidb':
                self.anidb = attributes['externalId']
            if attributes['externalSite'] == 'anilist':
                self.anilist = attributes['externalId']        
            if attributes['externalSite'] == 'myanimelist/anime':
                self.mal = attributes['externalId']          
            if attributes['externalSite'] == 'trakt':
                self.trakt = attributes['externalId']

    def getTraktFromTitle(self, titles, type, year):
        item = ''
        index = 0
        title_type = ['canon', 'english', 'romaji']
        try:
            while item == '':
                link = ''
                trakt_type = ''
                if type == 'TV':
                    link = self.api_path + self.search_tv
                    trakt_type = 'show'
                else:
                    link = self.api_path + self.search_movie
                    trakt_type = 'movie'
                resp = requests.get(link % titles[title_type[index]], headers=self.headers)
                load = json.loads(resp.content)
                for a in load:
                    for b in title_type:
                        if a[trakt_type]['title'] == titles[b] and str(a[trakt_type]['year']) == str(year):
                            item = a[trakt_type]
                        elif a[trakt_type]['title'] == titles[b]:
                            item = a[trakt_type]
                index += 1
                if item == '':
                    if len(load) == 1:
                        item = a[trakt_type]
        except:
            return
        if not item == '':
            try: self.trakt = item['ids']['trakt']
            except: self.trakt = ''
            try: self.imdb = item['ids']['imdb']
            except: self.imdb = ''
            try: self.tvdb = item['ids']['tvdb']
            except: self.tvdb = ''
            try: self.tmdb = item['ids']['tmdb']
            except: self.tmdb = ''            

    def getTrakt(self, id, type, titles):
        id_type = ''
        item = ''
        
        if type == 'TV':
            id_type = 'show'
        else:
            id_type = 'movie'
            
        resp = requests.get(self.api_path + self.search_trakt % (id, id_type), headers=self.headers)
        load = json.loads(resp.content)

        for a in load:
            if a['type'] == id_type:
                item = a[id_type]

        if not item == '':
            try: self.trakt = item['ids']['trakt']
            except: self.trakt = ''
            try: self.imdb = item['ids']['imdb']
            except: self.imdb = ''
            try: self.tvdb = item['ids']['tvdb']
            except: self.tvdb = ''
            try: self.tmdb = item['ids']['tmdb']
            except: self.tmdb = ''         
        
        