import requests
import json
import math

class source:
    def __init__(self):
        self.base_url = 'https://www.animefever.tv'
        self.search_url = 'https://www.animefever.tv/api/anime/listing?search=%s&sortBy=name+asc&hasVideos=true'
        self.episodes_url = 'https://www.animefever.tv/api/anime/details/episodes'
        self.source_url = 'https://www.animefever.tv/api/anime/episode/%s'
        
    def tvshow(self, data):
        resp = requests.get(self.search_url % data['mal_titles']['base'])
        load = json.loads(resp.content)
        data_resp = load['data']
        
        anime_id = ''
        anime_slug = ''
        
        for a in data_resp:
            if a['name'] == data['mal_titles']['base'] or a['alt_name'] == data['mal_titles']['base']:
                anime_id = a['id']
                anime_slug = a['slug']
                
        slug = '%s-%s' % (str(anime_id), anime_slug)
        page = int(math.ceil(float(data['episode'])/30))
        
        resp = requests.post(self.episodes_url, data={'id': slug, 'page': page})
        load = json.loads(resp.content)
        data_resp = load['data']
        
        episode_id = ''
        episode_slug = ''
        
        for a in data_resp:
            episode_number = int(float(a['number']))
            if int(data['episode']) == episode_number:
                episode_id = a['id']
                episode_slug = a['slug']
        
        episode_slug = '%s-%s' % (str(episode_id), episode_slug)
        
        return episode_slug
        
    def movie(self, data):
        resp = requests.get(self.search_url % data['mal_titles']['base'])
        load = json.loads(resp.content)
        data_resp = load['data']
        
        anime_id = ''
        anime_slug = ''
        
        for a in data_resp:
            if a['name'] == data['mal_titles']['base'] or a['alt_name'] == data['mal_titles']['base']:
                anime_id = a['id']
                anime_slug = a['slug']
                
        slug = '%s-%s' % (str(anime_id), anime_slug)
        page = int(math.ceil(float(data['episode'])/30))
        
        resp = requests.post(self.episodes_url, data={'id': slug, 'page': page})
        load = json.loads(resp.content)
        data_resp = load['data']
        
        episode_id = ''
        episode_slug = ''
        
        for a in data_resp:
            episode_number = int(float(a['number']))
            if episode_number == 1:
                episode_id = a['id']
                episode_slug = a['slug']
        
        episode_slug = '%s-%s' % (str(episode_id), episode_slug)
        
        return episode_slug

    def sources(self, data):
        source_list = []
        
        resp = requests.get(self.source_url % data)
        load = json.loads(resp.content)
        data_resp = load['data']

        subs = None
        sub_list = data_resp['subtitles']
        for a in sub_list:
            if a['label'] == 'English':
                subs = a['file']
        
        source = {'site': 'AnimeFever',
                  'source': 'AnimeFever',
                  'link': data_resp['stream'],
                  'quality': 360,
                  'audio_type': 'Sub',
                  'adaptive': False,
                  'subtitles': subs}                          
        source_list.append(source)

        return source_list