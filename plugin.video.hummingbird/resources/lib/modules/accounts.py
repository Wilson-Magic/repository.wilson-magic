import requests
import json
import re
import time

from resources.lib.modules import tools
from bs4 import BeautifulSoup

from resources.lib.modules import cache
from resources.lib.modules import kitsu_api
from resources.lib.modules.worker import ThreadPool

class Mappings:
    def __init__(self):
        self.return_sites = {
            'mal': {'notify': 'myanimelist/anime', 'hato': 'mal_id'},
            'kitsu': {'notify': 'kitsu/anime', 'hato': 'kitsu_id'},
            'anilist': {'notify': 'anilist/anime', 'hato': 'anilist_id'}}
            
        self.thread_list = ThreadPool()
        self.remaining_threads = []
        self.id_list = []

    def get(self, site, id, return_site):
        try:
            resp = requests.get('https://arm.now.sh/api/v1/search?type=%s&id=%s' % (site, id))
            load = json.loads(resp.content)
            return load['services'][return_site]
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
                    if a['service'] == self.return_sites[return_site]['notify']:
                        return a['serviceId']
            except:
                return data[self.return_sites[return_site]['hato']]    
            
    def get_thread(self, site, id, return_site):
        new_id = cache.hummingCache().cacheCheck(self.get, 8760, site, id, return_site)
        self.id_list.append({site: id, return_site: new_id})
        self.remaining_threads.remove(id)        
            
    def get_list(self, site, list, return_site):
        for a in list:
            self.remaining_threads.append(a)
            self.thread_list.put(self.get_thread, site, a, return_site)     

        while len(self.remaining_threads) > 0:
            time.sleep(1)
        
        sorted_list = []
        
        for a in list:
            for b in self.id_list:
                if b[site] == a:
                    sorted_list.append(b[return_site])
         
        return sorted_list                    
            
class Lists:
    def get(self, site, list):
        if site == 'kitsu' and list == 'current':
            anime = Kitsu().getCurrent()
        elif site == 'kitsu' and list == 'finished':
            anime = Kitsu().getFinished()
        elif site == 'kitsu' and list == 'dropped':
            anime = Kitsu().getDropped()
        elif site == 'kitsu' and list == 'on_hold':
            anime = Kitsu().getHold()
        elif site == 'kitsu' and list == 'planned':
            anime = Kitsu().getPlanned()        
        
        elif site == 'mal' and list == 'current':
            anime = Mal().getCurrent()
        elif site == 'mal' and list == 'finished':
            anime = Mal().getFinished()
        elif site == 'mal' and list == 'dropped':
            anime = Mal().getDropped()        
        elif site == 'mal' and list == 'on_hold':
            anime = Mal().getHold()
        elif site == 'mal' and list == 'planned':
            anime = Mal().getPlanned() 
        
        elif site == 'anilist' and list == 'current':
            anime = Anilist().getCurrent()
        elif site == 'anilist' and list == 'finished':
            anime = Anilist().getFinished()
        elif site == 'anilist' and list == 'dropped':
            anime = Anilist().getDropped()
        elif site == 'anilist' and list == 'on_hold':
            anime = Anilist().getHold()
        elif site == 'anilist' and list == 'planned':
            anime = Anilist().getPlanned() 
            
        return anime

class Kitsu:
    def __init__(self):
        self.client_id = 'dd031b32d2f56c990b1425efe6c42ad847e7fe3ab46bf1299f05ecd856bdb7dd'
        self.client_secret = '54d7307928f63414defd96399fc31ba847961ceaecef3a5fd93144e960c0e151'
        self.oauth = 'https://kitsu.io/api/oauth'
        self.headers = {'Accept': 'application/vnd.api+json',
                        'Content-Type': 'application/vnd.api+json'}
                        
        self.username = tools.getSetting('kitsu.user')
        self.email = tools.getSetting('kitsu.email')
        self.password = tools.getSetting('kitsu.pass')
        self.access = tools.getSetting('kitsu.access')
        self.refresh = tools.getSetting('kitsu.refresh')
        self.userid = tools.getSetting('kitsu.userid')

    def login(self, silent=False):
        try:
            login = requests.post(self.oauth + '/token', params={'grant_type': 'password', 'username': self.email, 'password': self.password}, headers=self.headers)
            info = json.loads(login.text)
            tools.setSetting('kitsu.access', str(info['access_token']))
            tools.setSetting('kitsu.refresh', str(info['refresh_token']))
            tools.setSetting('kitsu.create', str(info['created_at']))
            tools.setSetting('kitsu.expiry', str(info['expires_in']))
            user = requests.get('https://kitsu.io/api/edge/users?filter[name]=%s' % self.username, headers=self.headers)
            userdata = json.loads(user.content)
            userdata = userdata['data'][0]
            tools.setSetting('kitsu.userid', str(userdata['id']))
            if silent != True:
                tools.showDialog.notification(tools.addonName, 'Kitsu - Logged in successfully')
            else:
                tools.log('Kitsu - Logged in successfully')
        except:
            if silent != True:
                tools.showDialog.notification(tools.addonName, 'Kitsu - Login unsuccessful')
            else:
                tools.log('Kitsu - Login unsuccessful')
                
    def logout(self):
        tools.setSetting('kitsu.access', '')
        tools.setSetting('kitsu.refresh', '')
        tools.setSetting('kitsu.create', '')
        tools.setSetting('kitsu.expiry', '')
        tools.setSetting('kitsu.userid', '')
        tools.showDialog.notification(tools.addonName, 'Kitsu - Logged out successfully')        
        return

    def track(self, id, episode, status):
        self.headers['Authorization'] = 'Bearer %s' % self.access
    
        params = {
            "filter[user_id]": self.userid,
            "filter[anime_id]": id
            }        
        resp = requests.get('https://kitsu.io/api/edge/library-entries', headers=self.headers, params=params)
        scrobble = json.loads(resp.content)
        
        if len(scrobble['data']) == 0:
            params = {
                    "data": {
                        "type": "libraryEntries",
                        "attributes": {
                            'status': status,
                            'progress': int(episode)
                            },
                        "relationships":{
                            "user":{
                                "data":{
                                    "id": int(self.userid),
                                    "type": "users"
                                }
                           },
                        "anime":{
                            "data":{
                                "id": int(id),
                                "type": "anime"
                                }
                            }
                        }
                    }
                }

            resp = requests.post('https://kitsu.io/api/edge/library-entries', headers=self.headers, json=params)
            tools.log('%s - Successfully Scrobbled')
            return
            
        anime_id = scrobble['data'][0]['id']
        params = {
            'data': {
                'id': int(anime_id),
                'type': 'libraryEntries',
                'attributes': {
                    'progress': int(episode)
                    }
                }
            }
            
        resp = requests.patch('https://kitsu.io/api/edge/library-entries/%s' % anime_id, headers=self.headers, json=params)       
        return

    def getCurrent(self):
        status = 'current'
        
        sort_status = tools.getSetting('current.sort')
        sort = tools.account_sort['kitsu'][sort_status]
        
        params = {
            "fields[anime]": "slug,posterImage,coverImage,canonicalTitle,titles,synopsis,subtype,startDate,status,averageRating,popularityRank,ratingRank,episodeCount,episodeLength",
            "fields[users]": "id",
            "filter[user_id]": self.userid,
            "filter[kind]": "anime",
            "filter[status]": status,
            "include": "anime,user,mediaReaction",
            "page[limit]": "500",
            "page[offset]": "0",
            "sort": sort
            }
            
        anime = requests.get('https://kitsu.io/api/edge/library-entries', headers=self.headers, params=params)
        data = json.loads(anime.content)

        try: info = data['included'][1:]
        except: info = []
        
        extracted_items = kitsu_api.KitsuBrowser().extract_items(info)
        
        sortedItems = tools.sort_anime_by_json(extracted_items, info)

        return sortedItems

    def getFinished(self):
        status = 'completed'

        sort_status = tools.getSetting('finished.sort')
        sort = tools.account_sort['kitsu'][sort_status]
        
        params = {
            "fields[anime]": "slug,posterImage,coverImage,canonicalTitle,titles,synopsis,subtype,startDate,status,averageRating,popularityRank,ratingRank,episodeCount,episodeLength",
            "fields[users]": "id",
            "filter[user_id]": self.userid,
            "filter[kind]": "anime",
            "filter[status]": status,
            "include": "anime,user,mediaReaction",
            "page[limit]": "500",
            "page[offset]": "0",
            "sort": sort
            }
            
        anime = requests.get('https://kitsu.io/api/edge/library-entries', headers=self.headers, params=params)
        data = json.loads(anime.content)

        try: info = data['included'][1:]
        except: info = []

        extracted_items = kitsu_api.KitsuBrowser().extract_items(info)

        sortedItems = tools.sort_anime_by_json(extracted_items, info)

        return sortedItems

    def getDropped(self):
        status = 'dropped'

        sort_status = tools.getSetting('dropped.sort')
        sort = tools.account_sort['kitsu'][sort_status]
        
        params = {
            "fields[anime]": "slug,posterImage,coverImage,canonicalTitle,titles,synopsis,subtype,startDate,status,averageRating,popularityRank,ratingRank,episodeCount,episodeLength",
            "fields[users]": "id",
            "filter[user_id]": self.userid,
            "filter[kind]": "anime",
            "filter[status]": status,
            "include": "anime,user,mediaReaction",
            "page[limit]": "500",
            "page[offset]": "0",
            "sort": sort
            }
            
        anime = requests.get('https://kitsu.io/api/edge/library-entries', headers=self.headers, params=params)
        data = json.loads(anime.content)

        try: info = data['included'][1:]
        except: info = []

        extracted_items = kitsu_api.KitsuBrowser().extract_items(info)

        sortedItems = tools.sort_anime_by_json(extracted_items, info)

        return sortedItems
        
    def getHold(self):
        status = 'on_hold'

        sort_status = tools.getSetting('hold.sort')
        sort = tools.account_sort['kitsu'][sort_status]
        
        params = {
            "fields[anime]": "slug,posterImage,coverImage,canonicalTitle,titles,synopsis,subtype,startDate,status,averageRating,popularityRank,ratingRank,episodeCount,episodeLength",
            "fields[users]": "id",
            "filter[user_id]": self.userid,
            "filter[kind]": "anime",
            "filter[status]": status,
            "include": "anime,user,mediaReaction",
            "page[limit]": "500",
            "page[offset]": "0",
            "sort": sort
            }
            
        anime = requests.get('https://kitsu.io/api/edge/library-entries', headers=self.headers, params=params)
        data = json.loads(anime.content)

        try: info = data['included'][1:]
        except: info = []

        extracted_items = kitsu_api.KitsuBrowser().extract_items(info)

        sortedItems = tools.sort_anime_by_json(extracted_items, info)

        return sortedItems

    def getPlanned(self):
        status = 'planned'

        sort_status = tools.getSetting('planned.sort')
        sort = tools.account_sort['kitsu'][sort_status]
        
        params = {
            "fields[anime]": "slug,posterImage,coverImage,canonicalTitle,titles,synopsis,subtype,startDate,status,averageRating,popularityRank,ratingRank,episodeCount,episodeLength",
            "fields[users]": "id",
            "filter[user_id]": self.userid,
            "filter[kind]": "anime",
            "filter[status]": status,
            "include": "anime,user,mediaReaction",
            "page[limit]": "500",
            "page[offset]": "0",
            "sort": sort
            }
            
        anime = requests.get('https://kitsu.io/api/edge/library-entries', headers=self.headers, params=params)
        data = json.loads(anime.content)

        try: info = data['included'][1:]
        except: info = []

        extracted_items = kitsu_api.KitsuBrowser().extract_items(info)

        sortedItems = tools.sort_anime_by_json(extracted_items, info)

        return sortedItems

class Mal:
    def __init__(self):
        self.site = 'https://myanimelist.net'
        
        self.username = tools.getSetting('mal.user')
        self.password = tools.getSetting('mal.pass')
        
        self.logsessid = tools.getSetting('mal.logsess')
        self.sessionid = tools.getSetting('mal.sessionid')
        
        self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept': '*/*',
                'Cookie': 'MALHLOGSESSID=%s; MALSESSIONID=%s; is_logged_in=1; anime_update_advanced=1' % (self.logsessid, self.sessionid),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 \Firefox/56.0',
                }
    
    def login(self, silent=False):
        session = requests.session()
        crsf_res = session.get(self.site).text
        crsf = (re.compile("<meta name='csrf_token' content='(.+?)'>").findall(crsf_res))[0]
        payload = {
            "user_name": self.username,
            "password": self.password,
            "cookie": 1,
            "sublogin": "Login",
            "submit": 1,
            "csrf_token": crsf
            }        
        url = self.site + '/login.php?from=%2F'
        session.get(url)
        result = session.post(url, data=payload)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', attrs={'class': 'badresult'})
        if results:
            if silent != True:
                tools.showDialog.notification(tools.addonName, 'MAL - Login Unsuccessful')
            else:
                tools.log('MAL - Login Unsuccessful')
            return
        
        tools.setSetting('mal.logsess', str(session.cookies['MALHLOGSESSID']))
        tools.setSetting('mal.sessionid', str(session.cookies['MALSESSIONID']))
        
        if silent != True:
            tools.showDialog.notification(tools.addonName, 'MAL - Logged in successfully')
        else:
            tools.log('MAL - Logged in successfully')
        
        return

    def track(self, id, episode, status):
        mal_id = cache.hummingCache().cacheCheck(Mappings().get, 8760, 'kitsu', id, 'mal')
        
        result = requests.get(self.site + '/anime/%s' % mal_id, headers=self.headers)
        soup = BeautifulSoup(result.content, 'html.parser')
        csrf = soup.find('meta', {'name':'csrf_token'})['content']
        match = soup.find('h2', {'class':'mt8'})
        if match:
            url = self.site + '/ownlist/anime/edit.json'
        else:
            url = self.site + '/ownlist/anime/add.json'
            
        payload = {
            'anime_id': int(mal_id),
            'status': status,
            'num_watched_episodes': int(episode),
            'csrf_token': csrf
            }
            
        resp = requests.post(url, headers=self.headers, json=payload)

    def getCurrent(self):
        data_items = []
        mal_anime = []
        kitsu_ids = []
        
        sort_status = tools.getSetting('current.sort')
        sort = tools.account_sort['mal'][sort_status] % '1'
        
        resp = requests.get(self.site + '/animelist/%s?%s' % (self.username, sort))
        soup = BeautifulSoup(resp.content, 'html.parser')
        items = soup.find_all('table', attrs={'class': 'list-table'})
        
        for a in items:
            data_items = str(a.get('data-items'))
            data_items = data_items.replace('&quot;', '"')
            data_items = json.loads(data_items)
        for a in data_items:
            mal_anime.append(a['anime_id'])
        kitsu_ids = Mappings().get_list('mal', mal_anime, 'kitsu')
            
        anime_list = kitsu_api.KitsuBrowser().getListById(kitsu_ids)
        anime_list = tools.sort_anime_by_id(anime_list, kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        if '-' in sort_status:
            anime_list = sorted(anime_list, reverse=True)
        
        return anime_list

    def getFinished(self):
        data_items = []
        mal_anime = []
        kitsu_ids = []
        
        sort_status = tools.getSetting('finished.sort')
        sort = tools.account_sort['mal'][sort_status] % '2'       
        
        resp = requests.get(self.site + '/animelist/%s?%s' % (self.username, sort))
        soup = BeautifulSoup(resp.content, 'html.parser')
        items = soup.find_all('table', attrs={'class': 'list-table'})
        
        for a in items:
            data_items = str(a.get('data-items'))
            data_items = data_items.replace('&quot;', '"')
            data_items = json.loads(data_items)
        for a in data_items:
            mal_anime.append(a['anime_id'])
        kitsu_ids = Mappings().get_list('mal', mal_anime, 'kitsu')
            
        anime_list = kitsu_api.KitsuBrowser().getListById(kitsu_ids)
        anime_list = tools.sort_anime_by_id(anime_list, kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime

        if '-' in sort_status:
            anime_list = sorted(anime_list, reverse=True)        
        
        return anime_list

    def getDropped(self):
        data_items = []
        mal_anime = []
        kitsu_ids = []
        
        sort_status = tools.getSetting('dropped.sort')
        sort = tools.account_sort['mal'][sort_status] % '4'
        
        resp = requests.get(self.site + '/animelist/%s?%s' % (self.username, sort))
        soup = BeautifulSoup(resp.content, 'html.parser')
        items = soup.find_all('table', attrs={'class': 'list-table'})
        
        for a in items:
            data_items = str(a.get('data-items'))
            data_items = data_items.replace('&quot;', '"')
            data_items = json.loads(data_items)
        for a in data_items:
            mal_anime.append(a['anime_id'])
        kitsu_ids = Mappings().get_list('mal', mal_anime, 'kitsu')
            
        anime_list = kitsu_api.KitsuBrowser().getListById(kitsu_ids)
        anime_list = tools.sort_anime_by_id(anime_list, kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime

        if '-' in sort_status:
            anime_list = sorted(anime_list, reverse=True)
        
        return anime_list
        
    def getHold(self):
        data_items = []
        mal_anime = []
        kitsu_ids = []
        
        sort_status = tools.getSetting('hold.sort')
        sort = tools.account_sort['mal'][sort_status] % '3'
        
        resp = requests.get(self.site + '/animelist/%s?%s' % (self.username, sort))
        soup = BeautifulSoup(resp.content, 'html.parser')
        items = soup.find_all('table', attrs={'class': 'list-table'})
        
        for a in items:
            data_items = str(a.get('data-items'))
            data_items = data_items.replace('&quot;', '"')
            data_items = json.loads(data_items)
        for a in data_items:
            mal_anime.append(a['anime_id'])
        kitsu_ids = Mappings().get_list('mal', mal_anime, 'kitsu')
            
        anime_list = kitsu_api.KitsuBrowser().getListById(kitsu_ids)
        anime_list = tools.sort_anime_by_id(anime_list, kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        if '-' in sort_status:
            anime_list = sorted(anime_list, reverse=True)        
        
        return anime_list
        
    def getPlanned(self):
        data_items = []
        mal_anime = []
        kitsu_ids = []
        
        sort_status = tools.getSetting('planned.sort')
        sort = tools.account_sort['mal'][sort_status] % '6'
        
        resp = requests.get(self.site + '/animelist/%s?%s' % (self.username, sort))
        soup = BeautifulSoup(resp.content, 'html.parser')
        items = soup.find_all('table', attrs={'class': 'list-table'})
        
        for a in items:
            data_items = str(a.get('data-items'))
            data_items = data_items.replace('&quot;', '"')
            data_items = json.loads(data_items)
        for a in data_items:
            mal_anime.append(a['anime_id'])
        kitsu_ids = Mappings().get_list('mal', mal_anime, 'kitsu')  
            
        anime_list = kitsu_api.KitsuBrowser().getListById(kitsu_ids)
        anime_list = tools.sort_anime_by_id(anime_list, kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime

        if '-' in sort_status:
            anime_list = sorted(anime_list, reverse=True)

        return anime_list

class Anilist:
    def __init__(self):
        self.site = "https://graphql.anilist.co"
        
        self.username = tools.getSetting('ani.user')
        self.password = tools.getSetting('ani.pass')
        
        self.user_id = tools.getSetting('ani.userid')
        
        self.headers = {
            'Authorization': 'Bearer ' + self.password,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            }

    def login(self, silent=False):
        query = '''
        query ($name: String) {
            User(name: $name) {
                id
                }
            }
        '''

        variables = {
            "name": self.username
            }
            
        resp = requests.post(self.site, json={'query': query, 'variables': variables})
        results = json.loads(resp.content)
        if results.has_key('errors'):
            if silent != True:
                tools.showDialog.notification(tools.addonName, 'AniList - Login unsuccessful')
            else:
                tools.log('Anilist - Login unsuccessful')
            return
        
        tools.setSetting('ani.userid', str(results['data']['User']['id']))
        if silent != True:
            tools.showDialog.notification(tools.addonName, 'AniList - Logged in successfully')
        else:
            tools.log('Anilist - Logged in successfully')
        return

    def track(self, id, episode, status):
        anilist_id = cache.hummingCache().cacheCheck(Mappings().get, 8760, 'kitsu', id, 'anilist')
        
        query = '''
        mutation ($mediaId: Int, $progress : Int, $status: MediaListStatus) {
            SaveMediaListEntry (mediaId: $mediaId, progress: $progress, status: $status) {
                id
                progress
                status
                }
            }
        '''

        variables = {
            'mediaId': int(anilist_id),
            'progress': int(episode),
            'status': status
            }
        
        resp = requests.post(self.site, headers=self.headers, json={'query': query, 'variables': variables})

    def getCurrent(self):
        anilist_items = []
        kitsu_ids = []
        
        status = 'CURRENT'

        sort_status = tools.getSetting('current.sort')
        sort = tools.account_sort['anilist'][sort_status]
        
        query = '''
        query ($userId: Int, $userName: String, $status: MediaListStatus, $type: MediaType, $sort: [MediaListSort]) {
            MediaListCollection(userId: $userId, userName: $userName, status: $status, type: $type, sort: $sort) {
                lists {
                    entries {
                        ...mediaListEntry
                        }
                    }
                }
            }
        fragment mediaListEntry on MediaList {
            id
            mediaId
            status
            progress
            customLists
            media {
                id
                title {
                    userPreferred
                }
                coverImage {
                    extraLarge
                }
                status
                episodes
            }
        }
        '''

        variables = {
            'userId': int(self.user_id),
            'username': self.username,
            'status': status,
            'type': 'ANIME',
            'sort': [sort]
            }

        resp = requests.post(self.site, json={'query': query, 'variables': variables})
        results = json.loads(resp.content)
        if results.has_key('errors'):
            return
        
        try: entries = results['data']['MediaListCollection']['lists'][0]['entries']
        except: entries = []
        
        for a in entries:
            anilist_items.append(a['media']['id'])
        kitsu_ids = Mappings.get_list('anilist', anilist_items, 'kitsu')
        
        anime_list = kitsu_api.KitsuBrowser().getListById(kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        anime_list = tools.sort_anime_by_id(anime_list, kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        if '-' in sort_status:
            anime_list = sorted(anime_list, reverse=True)
        
        return anime_list

    def getFinished(self):
        anilist_items = []
        kitsu_ids = []
        
        status = 'COMPLETED'

        sort_status = tools.getSetting('finished.sort')
        sort = tools.account_sort['anilist'][sort_status]
        
        query = '''
        query ($userId: Int, $userName: String, $status: MediaListStatus, $type: MediaType, $sort: [MediaListSort]) {
            MediaListCollection(userId: $userId, userName: $userName, status: $status, type: $type, sort: $sort) {
                lists {
                    entries {
                        ...mediaListEntry
                        }
                    }
                }
            }
        fragment mediaListEntry on MediaList {
            id
            mediaId
            status
            progress
            customLists
            media {
                id
                title {
                    userPreferred
                }
                coverImage {
                    extraLarge
                }
                status
                episodes
            }
        }
        '''

        variables = {
            'userId': int(self.user_id),
            'username': self.username,
            'status': status,
            'type': 'ANIME',
            'sort': [sort]
            }

        resp = requests.post(self.site, json={'query': query, 'variables': variables})
        results = json.loads(resp.content)
        if results.has_key('errors'):
            return
        
        try: entries = results['data']['MediaListCollection']['lists'][0]['entries']
        except: entries = []
        
        for a in entries:
            anilist_items.append(a['media']['id'])
        kitsu_ids = Mappings.get_list('anilist', anilist_items, 'kitsu')
        
        anime_list = kitsu_api.KitsuBrowser().getListById(kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        anime_list = tools.sort_anime_by_id(anime_list, kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        if '-' in sort_status:
            anime_list = sorted(anime_list, reverse=True)        
        
        return anime_list

    def getDropped(self):
        anilist_items = []
        kitsu_ids = []
        
        status = 'DROPPED'
        sort_status = tools.getSetting('dropped.sort')
        sort = tools.account_sort['anilist'][sort_status]
        
        query = '''
        query ($userId: Int, $userName: String, $status: MediaListStatus, $type: MediaType, $sort: [MediaListSort]) {
            MediaListCollection(userId: $userId, userName: $userName, status: $status, type: $type, sort: $sort) {
                lists {
                    entries {
                        ...mediaListEntry
                        }
                    }
                }
            }
        fragment mediaListEntry on MediaList {
            id
            mediaId
            status
            progress
            customLists
            media {
                id
                title {
                    userPreferred
                }
                coverImage {
                    extraLarge
                }
                status
                episodes
            }
        }
        '''

        variables = {
            'userId': int(self.user_id),
            'username': self.username,
            'status': status,
            'type': 'ANIME',
            'sort': [sort]
            }

        resp = requests.post(self.site, json={'query': query, 'variables': variables})
        results = json.loads(resp.content)
        if results.has_key('errors'):
            return
        
        try: entries = results['data']['MediaListCollection']['lists'][0]['entries']
        except: entries = []
        
        for a in entries:
            anilist_items.append(a['media']['id'])
        kitsu_ids = Mappings.get_list('anilist', anilist_items, 'kitsu')
        
        anime_list = kitsu_api.KitsuBrowser().getListById(kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        anime_list = tools.sort_anime_by_id(anime_list, kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        if '-' in sort_status:
            anime_list = sorted(anime_list, reverse=True)
        
        return anime_list

    def getHold(self):
        anilist_items = []
        kitsu_ids = []
        
        status = 'PAUSED'

        sort_status = tools.getSetting('hold.sort')
        sort = tools.account_sort['anilist'][sort_status]
        
        query = '''
        query ($userId: Int, $userName: String, $status: MediaListStatus, $type: MediaType, $sort: [MediaListSort]) {
            MediaListCollection(userId: $userId, userName: $userName, status: $status, type: $type, sort: $sort) {
                lists {
                    entries {
                        ...mediaListEntry
                        }
                    }
                }
            }
        fragment mediaListEntry on MediaList {
            id
            mediaId
            status
            progress
            customLists
            media {
                id
                title {
                    userPreferred
                }
                coverImage {
                    extraLarge
                }
                status
                episodes
            }
        }
        '''

        variables = {
            'userId': int(self.user_id),
            'username': self.username,
            'status': status,
            'type': 'ANIME',
            'sort': [sort]
            }

        resp = requests.post(self.site, json={'query': query, 'variables': variables})
        results = json.loads(resp.content)
        if results.has_key('errors'):
            return
        
        try: entries = results['data']['MediaListCollection']['lists'][0]['entries']
        except: entries = []
        
        for a in entries:
            anilist_items.append(a['media']['id'])
        kitsu_ids = Mappings.get_list('anilist', anilist_items, 'kitsu')
        
        anime_list = kitsu_api.KitsuBrowser().getListById(kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        anime_list = tools.sort_anime_by_id(anime_list, kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        if '-' in sort_status:
            anime_list = sorted(anime_list, reverse=True)
        
        return anime_list

    def getPlanned(self):
        anilist_items = []
        kitsu_ids = []
        
        status = 'PLANNING'

        sort_status = tools.getSetting('planned.sort')
        sort = tools.account_sort['anilist'][sort_status]
        
        query = '''
        query ($userId: Int, $userName: String, $status: MediaListStatus, $type: MediaType, $sort: [MediaListSort]) {
            MediaListCollection(userId: $userId, userName: $userName, status: $status, type: $type, sort: $sort) {
                lists {
                    entries {
                        ...mediaListEntry
                        }
                    }
                }
            }
        fragment mediaListEntry on MediaList {
            id
            mediaId
            status
            progress
            customLists
            media {
                id
                title {
                    userPreferred
                }
                coverImage {
                    extraLarge
                }
                status
                episodes
            }
        }
        '''

        variables = {
            'userId': int(self.user_id),
            'username': self.username,
            'status': status,
            'type': 'ANIME',
            'sort': [sort]
            }

        resp = requests.post(self.site, json={'query': query, 'variables': variables})
        results = json.loads(resp.content)
        if results.has_key('errors'):
            return
        
        try: entries = results['data']['MediaListCollection']['lists'][0]['entries']
        except: entries = []
        
        for a in entries:
            anilist_items.append(a['media']['id'])
        kitsu_ids = Mappings.get_list('anilist', anilist_items, 'kitsu')
        
        anime_list = kitsu_api.KitsuBrowser().getListById(kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        anime_list = tools.sort_anime_by_id(anime_list, kitsu_ids)
        
        tools.log(anime_list, 'error') #Should print list of anime
        
        if '-' in sort_status:
            anime_list = sorted(anime_list, reverse=True)
        
        return anime_list    