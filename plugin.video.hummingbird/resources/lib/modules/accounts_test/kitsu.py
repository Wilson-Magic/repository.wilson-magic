import requests
import json

from . import account_info
from resources.lib.modules import tools
from resources.lib.modules import kitsu_api

#KITSU WORKED BEFORE SO EVERYTHING IS LEFT THE SAME

class List:
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
        progress = data['data'] 
        
        mapped = account_info.map_to_item(progress, info)       
                
        extracted_items = kitsu_api.KitsuBrowser().extract_items(mapped)
        
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
        progress = data['data'] 
        
        mapped = account_info.map_to_item(progress, info)       
                
        extracted_items = kitsu_api.KitsuBrowser().extract_items(mapped)

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
        progress = data['data'] 
        
        mapped = account_info.map_to_item(progress, info)       
                
        extracted_items = kitsu_api.KitsuBrowser().extract_items(mapped)

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
        progress = data['data'] 
        
        mapped = account_info.map_to_item(progress, info)       
                
        extracted_items = kitsu_api.KitsuBrowser().extract_items(mapped)

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
        progress = data['data'] 
        
        mapped = account_info.map_to_item(progress, info)       
                
        extracted_items = kitsu_api.KitsuBrowser().extract_items(mapped)

        sortedItems = tools.sort_anime_by_json(extracted_items, info)

        return sortedItems

            
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

