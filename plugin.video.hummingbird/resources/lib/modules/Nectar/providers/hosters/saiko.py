import requests
import re

class source:
    def __init__(self):
        self.base_url = 'https://saiko.vip/'
        self.search_url = '?url=search&query=%s'
        self.episode_url = '?/anime/episode?id=%s&ep=%s'
        
    def tvshow(self, data):
        resp = requests.get(self.base_url + self.search_url % data['titles']['canon'], headers={'referer': 'https://saiko.com/', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'})
        load = str(resp.content)

        anime = re.findall(r'<a class="d-block mb-3"(.*?)>', load)
        
        correct_id = ''
        
        for a in anime:
            anime_data = re.findall(r'href="\/\?\/anime\/\?id=(.*?)" title="(.*?)"', a)[0]
            if anime_data[1] == data['titles']['canon']:
                correct_id = anime_data[0]
                
        return self.episode_url % (correct_id, str(data['episode']))
            
    def movie(self, data):
        resp = requests.get(self.base_url + self.search_url % data['titles']['canon'], headers={'referer': 'https://saiko.com/', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'})
        load = str(resp.content)

        anime = re.findall(r'<a class="d-block mb-3"(.*?)>', load)
        
        correct_id = ''
        
        for a in anime:
            anime_data = re.findall(r'href="\/\?\/anime\/\?id=(.*?)" title="(.*?)"', a)[0]
            if anime_data[1] == data['titles']['canon']:
                correct_id = anime_data[0]
                
        return self.episode_url % (correct_id, '1')    

    def sources(self, data):
        resp = requests.get(self.base_url + data, headers={'referer': 'https://saiko.com/', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'})
        load = str(resp.content)

        options = re.findall(r'<span class="inner" title="(.*?)".*?</span><span class="badge">(.*?)</span>', load)

        source_list = []
        
        for a in options:
            if a[1] == 'Subbed': sub = 'Sub'
            else: sub = 'Dub'
            
            source = {'site': 'Saiko',
                      'source': 'Hexck',
                      'link': a[0],
                      'quality': 360,
                      'audio_type': sub, 
                      'adaptive': False,
                      'subtitles': None}
            source_list.append(source)
        
        return source_list      
            
id = source().tvshow({'titles': {'canon': 'Mikakunin de Shinkoukei'}, 'episode': '1'})
srcs = source().sources(id)            
print(srcs)
