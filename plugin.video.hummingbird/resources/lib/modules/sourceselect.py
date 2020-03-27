from resources.lib.modules import tools
from resources.lib.modules import sorting

class Selection:
    def __init__(self):
        self.working_link = False
        self.stream_link = ''
        
    def select(self, source_select, audio_type, sources):
        if sources is None:
            tools.showDialog.notification(tools.addonName, 'No sources found.')
            return None
            
        sortedSources = sorting.SortSources().sort(sources, audio_type)
        
        if len(sortedSources) == 0:
            tools.showDialog.notification(tools.addonName, 'No sources available on current settings.')
            return None
        
        streamLink = ''
        
        settingPlayback = tools.getSetting('play.type')

        sourceSelect = False
        
        if settingPlayback == 'Source Select':
            sourceSelect = True
        if source_select == True:
            sourceSelect = True
        
        if sourceSelect == True:
            list = []
            for a in sortedSources:
                list.append('%s | %s | %s | %s' % (a['quality'], a['site'], a['source'], a['audio_type']))
            while self.working_link is False:
                selection = tools.showDialog.select(tools.addonName + ': Source Select', list)
                if selection  == -1:                
                    return
                streamLink = sortedSources[selection]
                self.resolve_link(streamLink)
        else:
            index = 0
            while self.working_link is False:
                streamLink = sortedSources[index]
                self.resolve_link(streamLink)
                if self.working_link is False:
                    index += 1

        return {'url': self.stream_link, 'adaptive': streamLink['adaptive'], 'subtitles': self.subtitles_link}   
        
    def resolve_link(self, link):
        from resources.lib.modules import resolver
        
        stream_link = link['link']
        self.subtitles_link = link['subtitles']
        response = resolver.Resolver().resolve(link)
        
        if response['test_result'] == 'Good':
            self.working_link = True
            self.stream_link = response['resolved_url']
        else:
            self.working_link = False
            
                                