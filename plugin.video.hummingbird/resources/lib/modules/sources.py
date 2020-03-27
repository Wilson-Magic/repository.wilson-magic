import json
from resources.lib.modules import tools

class GetSources:
    def __init__(self):
        self.sources = []
        self.scrape_type = ''
        
    def scrape(self, args):
        info = json.loads(tools.unquote(args))
        
        try:
            title = info['episode_title']
            self.scrape_type = 'show'
        except:
            self.scrape_type = 'movie'

        if self.scrape_type == 'movie':
            scrape_data = {
                'titles': info['titles'],
                'mal_titles': info['mal_titles'],
                'year': info['year'], 
                'id':info['id']}
        else:
            scrape_data = {
                'titles': info['titles'],
                'mal_titles': info['mal_titles'],
                'year': info['year'],
                'season': info['seasonNumber'],
                'episode': info['episodeNumber'],
                'id': info['id']}
             
        from resources.lib.modules.Nectar import NectarScraper
        
        self.sources = NectarScraper().scrape(scrape_data)
        
        return self.sources
  
        
