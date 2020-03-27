# -*- coding: UTF-8 -*-

#Coded by Wilson Magic for the Hummingbird addon
#Based on the Exodus standard but is incompatible with other scrapers without modification

#Scraper: AnimePahe
#Site: animepahe.com

#Creation Date: 30/08/2019
#Last Update: 01/09/2019

import requests
import json

import math

#from resources.lib.modules import tools

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['animepahe.com']
        self.base_link = 'https://www.animepahe.com'
        self.api_search = 'api?m=search&l=8&q=%s'
        self.api_episodes = 'api?m=release&id=%s&l=30&sort=episode_asc&page=%s'
        self.api_embed = 'https://animepahe.com/api?m=embed&id=%s&session=%s&p=kwik'
        
        self.name_standard = 'canon'
        
    def tvshow(self, data):
        api = self.base_link + '/' + self.api_search % data['titles'][self.name_standard]
        response = requests.get(api).content
        load = json.loads(response)
        load_data = load['data']
        
        title = ''
        id = ''
        
        for a in load_data:
            for b in data['mal_titles']:
                if a['title'] == data['mal_titles'][b]:
                    title = a['title']
                    id = a['id']
        
        api = self.base_link + '/' + self.api_episodes % (id, '1')
        response = requests.get(api).content
        load = json.loads(response)
        
        episode = data['episode']
        
        page = int(math.ceil(float(int(episode))/30))
        
        api = self.base_link + '/' + self.api_episodes % (id, str(page))
        response = requests.get(api).content
        load = json.loads(response)
        
        load_data = load['data']
        
        ep_num = ''
        ep_id = ''
        sess = ''
        
        for a in load_data:
            if int(a['episode']) == int(episode):
                ep_num = int(a['episode'])
                ep_id = a['anime_id']
                sess = a['session']
                
        if ep_id == '':
            episode_number = episode
            if episode > 30:
                episode_number -= 30
            episode_item = load_data[episode_number-1]
            ep_num = int(episode_item['episode'])
            ep_id = episode_item['anime_id']
            sess = episode_item['session']
        
        api = self.api_embed % (ep_id, sess)
        
        return api
        
    def movie(self, data):
        api = self.base_link + '/' + self.api_search % data['titles'][self.name_standard]
        response = requests.get(api).content
        load = json.loads(response)
        load_data = load['data']
        
        title = ''
        id = ''
        
        for a in load_data:
            for b in data['titles']:
                if a['title'] == data['titles'][b]:
                    title = a['title']
                    id = a['id']
        
        api = self.base_link + '/' + self.api_episodes % (id, '1')
        response = requests.get(api).content
        load = json.loads(response)
        
        load_data = load['data'][0]
        
        ep_num = int(load_data['episode'])
        ep_id = load_data['id']
        sess = load_data['session']
        
        api = self.api_embed % (ep_id, sess)
        
        return api
                
    def sources(self, link):
        resp = requests.get(link)
        info = json.loads(resp.content)
        
        info = info['data']

        sources = []
        
        for a in info:
            quality = info[a]
            for b in quality:
                file_data = info[a][b]
                source = {'site': 'AnimePahe',
                          'source': 'Kwik.cx',
                          'link': file_data['url'],
                          'quality': int(b),
                          'audio_type': 'Sub', 
                          'adaptive': False,
                          'subtitles': None}
                sources.append(source)

        return sources       
