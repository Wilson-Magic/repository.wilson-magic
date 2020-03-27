# -*- coding: UTF-8 -*-

#Coded by Wilson Magic for the Hummingbird addon
#Based on the Exodus standard but is incompatible with other scrapers without modification

#Scraper: AnimeTwist
#Site: twist.moe

#Creation Date: 01/09/2019
#Last Update: 01/09/2019

import requests
import json

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['twist.moe']
        self.base_link = 'https://twist.moe/'
        self.api_search = 'api/anime'
        self.api_sources = 'api/anime/%s/sources'
        
        self.access_token = '1rj2vRtegS8Y60B3w3qNZm5T2Q0TN2NR'
        
        self.header = {'x-access-token': self.access_token}
        
    def tvshow(self, data):
        resp = requests.get(self.base_link + self.api_search, headers=self.header)
        load = json.loads(resp.content)

        correctItem = ''

        for a in load:
            for b in data['titles']:
                if a['title'] == data['titles'][b]:
                    correctItem = a
                    break
        
        search_url = self.base_link + self.api_sources % correctItem['slug']['slug']
        resp = requests.get(search_url, headers=self.header)
        load = json.loads(resp.content)
        episode = load[int(data['episode'])-1]

        link = {
            'slug': correctItem['slug']['slug'],
            'episode': data['episode'],
            'source': episode['source']
        }

        return json.dumps(link)

    def movie(self, data):
        resp = requests.get(self.base_link + self.api_search, headers=self.header)
        load = json.loads(resp.content)

        correctItem = ''

        for a in load:
            for b in data['titles']:
                if a['title'] == data['titles'][b]:
                    correctItem = a
                    break

        search_url = self.base_link + self.api_sources % correctItem['slug']['slug']
        resp = requests.get(search_url, headers=self.header)
        load = json.loads(resp.content)
        movie = load[0]
        source = movie['source']

        link = {
            'slug': correctItem['slug']['slug'],
            'episode': '1',
            'source': source
        }

        return json.dumps(link)
                
    def sources(self, link):
        sources = []
 
        source = {'site': 'AnimeTwist',
                  'source': 'Twist.moe',
                  'link': 'magictwist.wm/' + link,
                  'quality': 480,
                  'audio_type': 'Sub',
                  'adaptive': False,
                  'subtitles': None}         
        
        sources.append(source)

        return sources