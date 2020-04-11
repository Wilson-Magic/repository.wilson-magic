import requests
import json
import re

from . import account_info
from resources.lib.modules import tools

class List:
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

    def getCurrent(self):
        anilist_items = []
        kitsu_ids = []
        
        status = 'CURRENT'

        sort_status = tools.getSetting('current.sort')
        sort = account_info.account_sort['anilist'][sort_status]
        
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
                    romaji
                    english
                    native
                }
                format  
                episodes    
                status   
                description  
                seasonYear   
                genres                
                coverImage {
                    extraLarge
                    }
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
        if 'errors' in results:
            return
        
        try: entries = results['data']['MediaListCollection']['lists'][0]['entries']
        except: entries = []
        
        for a in entries:
            anilist_items.append({'id': a['media']['id'], 'status': 'current', 'progress': a['progress'], 'media': a['media']})
            
        anilist_data = Anilist().get_data(anilist_items)       
        
        if '-' in sort_status:
            anilist_data = sorted(anilist_data, reverse=True)
        
        return anilist_data
        
    def getFinished(self):
        anilist_items = []
        kitsu_ids = []
        
        status = 'COMPLETED'

        #sort_status = tools.getSetting('finished.sort')
        #sort = account_info.account_sort['anilist'][sort_status]
        
        sort_status = ''
        sort = 'PROGRESS'
        
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
                    romaji
                    english
                    native
                }
                format  
                episodes    
                status   
                description  
                seasonYear   
                genres                
                coverImage {
                    extraLarge
                    }
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
        if 'errors' in results:
            return
        
        try: entries = results['data']['MediaListCollection']['lists'][0]['entries']
        except: entries = []
        
        for a in entries:
            anilist_items.append({'id': a['media']['id'], 'status': 'current', 'progress': a['progress'], 'media': a['media']})
            
        anilist_data = Anilist().get_data(anilist_items)       
        
        if '-' in sort_status:
            anilist_data = sorted(anilist_data, reverse=True)
        
        return anilist_data

    def getDropped(self):
        anilist_items = []
        kitsu_ids = []
        
        status = 'DROPPED'

        sort_status = tools.getSetting('dropped.sort')
        sort = account_info.account_sort['anilist'][sort_status]
        
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
                    romaji
                    english
                    native
                }
                format  
                episodes    
                status   
                description  
                seasonYear   
                genres                
                coverImage {
                    extraLarge
                    }
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
        if 'errors' in results:
            return
        
        try: entries = results['data']['MediaListCollection']['lists'][0]['entries']
        except: entries = []
        
        for a in entries:
            anilist_items.append({'id': a['media']['id'], 'status': 'current', 'progress': a['progress'], 'media': a['media']})
            
        anilist_data = Anilist().get_data(anilist_items)       
        
        if '-' in sort_status:
            anilist_data = sorted(anilist_data, reverse=True)
        
        return anilist_data

    def getHold(self):
        anilist_items = []
        kitsu_ids = []
        
        status = 'PAUSED'

        sort_status = tools.getSetting('hold.sort')
        sort = account_info.account_sort['anilist'][sort_status]
        
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
                    romaji
                    english
                    native
                }
                format  
                episodes    
                status   
                description  
                seasonYear   
                genres                
                coverImage {
                    extraLarge
                    }
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
        if 'errors' in results:
            return
        
        try: entries = results['data']['MediaListCollection']['lists'][0]['entries']
        except: entries = []
        
        for a in entries:
            anilist_items.append({'id': a['media']['id'], 'status': 'current', 'progress': a['progress'], 'media': a['media']})
            
        anilist_data = Anilist().get_data(anilist_items)       
        
        if '-' in sort_status:
            anilist_data = sorted(anilist_data, reverse=True)
        
        return anilist_data

    def getPlanned(self):
        anilist_items = []
        kitsu_ids = []
        
        status = 'PLANNING'

        sort_status = tools.getSetting('planned.sort')
        sort = account_info.account_sort['anilist'][sort_status]
        
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
                    romaji
                    english
                    native
                }
                format  
                episodes    
                status   
                description  
                seasonYear   
                genres                
                coverImage {
                    extraLarge
                    }
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
        if 'errors' in results:
            return
        
        try: entries = results['data']['MediaListCollection']['lists'][0]['entries']
        except: entries = []
        
        for a in entries:
            anilist_items.append({'id': a['media']['id'], 'status': 'current', 'progress': a['progress'], 'media': a['media']})
            
        anilist_data = Anilist().get_data(anilist_items)       
        
        if '-' in sort_status:
            anilist_data = sorted(anilist_data, reverse=True)
        
        return anilist_data


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

    def get_data(self, list):
        got_data = []
        for a in list:
            got_data.append(self.get_info(a['media'], a['status'], a['progress']))
            
        return got_data            
    
    def get_info(self, data, watch_status, progress):
        dict = {
            'id': data['id'],
            'titles': {
                 'base': data['title']['romaji'], 
                 'english': data['title']['english'], 
                 'japanese': data['title']['native']
                 },
            'subtype': data['format'],
            'episode_count': data['episodes'],
            'status': data['status'],
            'plot': data['description'],
            'year': data['seasonYear'],
            'genres': ', '.join(data['genres']),
            'picture': data['coverImage']['extraLarge'],
            'account_info': {
                'status': watch_status,
                'progress': progress
                }
            }
        
        return dict
