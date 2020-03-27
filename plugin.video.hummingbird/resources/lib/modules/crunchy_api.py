import requests
import json
import re

class CrunchyrollAPI:
    def __init__(self):
        self.session_id = self.get_crunchy_session()
    
        self.autocomplete = 'https://api.crunchyroll.com/autocomplete.0.json?media_types=anime&q=%s&filter=alpha&limit=10000&session_id=%s'
        self.list_collections = 'https://api.crunchyroll.com/list_collections.0.json?series_id=%s&session_id=%s'
        
    def get_crunchy_session(self):
        sess = requests.session()
        resp = sess.get('https://www.crunchyroll.com/en-gb/login')
        cookie = sess.cookies['session_id']
        return cookie

    def search(self, slug):
        url = self.autocomplete % (slug, self.session_id)
        resp = requests.get(url)
        load = json.loads(resp.content)
        data = load['data']
        
        name = ''
        series_id = ''
        
        for a in data:
            url = a['url']
            a_slug = url.split('/')[4]
            if slug == a_slug:
                name = a['name']
                series_id = a['series_id']
        
        url = self.list_collections % (series_id, self.session_id)
        resp = requests.get(url)
        load = json.loads(resp.content)
        data = load['data']
       
        names = []
       
        for a in data:
            names.append(a['name'])
       
        return names
         
