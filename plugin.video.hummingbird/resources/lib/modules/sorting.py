from resources.lib.modules import tools

class SortSources:
    def __init__(self):
        #Audio
        self.audio_exclusion = tools.getSetting('sort.exclusion')
        self.audio_preference = tools.getSetting('sort.audio')
        #Quality
        self.minimum_quality = tools.getSetting('sort.minq')
        self.maximum_quality = tools.getSetting('sort.maxq')
        #Scrapers
        self.legitimate_preference = tools.getSetting('legit.prefer')
        self.site_preference = tools.getSetting('site.prefer')
        
        self.sources = []
        
    def sort(self, sources, audio_type):
        self.sources = sources
         
        self.translate_settings(audio_type)
        self.exclude_quality()
        self.exclude_audio()

        if self.legitimate_preference == False:
            self.sources = sorted(self.sources, key=lambda x: (x['site']==self.site_preference, x['audio_type']==self.audio_preference, x['quality']), reverse=True)
        else:
            self.sources = sorted(self.sources, key=lambda x: (x['audio_type']==self.audio_preference, x['source']=='Crunchyroll', x['source']=='FastStream', x['source']=='Funimation', x['site']==self.site_preference, x['quality']), reverse=True)
            
        return self.sources

        
    def exclude_quality(self):
        sources = []
        
        for a in self.sources:
            if a['quality'] >= self.minimum_quality and a['quality'] <= self.maximum_quality:
                sources.append(a)  
        
        self.sources = sources
        
    def exclude_audio(self):
        sources = []
        
        if self.audio_exclusion != None:
            for a in self.sources:
                if a['audio_type'] != self.audio_exclusion:
                    sources.append(a)
        else:
            sources = self.sources
            
        self.sources = sources
    
    def translate_settings(self, type):
        if self.audio_exclusion == 'None':
            self.audio_exclusion = None
            
        if type != None:
            self.audio_exclusion = type

        self.minimum_quality = int(self.minimum_quality)
        self.maximum_quality = int(self.maximum_quality)
        
        if self.legitimate_preference == 'false':
            self.legitimate_preference = False
        elif self.legitimate_preference == 'true':
            self.legitimate_preference = True
        
        
        
        
    
    