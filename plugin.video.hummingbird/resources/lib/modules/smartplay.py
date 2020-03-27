import json

from resources.lib.menus import anime
from resources.lib.modules import tools
from resources.lib.modules import kitsu_api

class SmartPlay:
    def __init__(self):
        self.actionArgs = ''
        self.sourceSelect = ''
        self.audioType = ''
        self.episodes = []
        
    def smartPlay(self, args, source_select, audio_type):
        self.preliminaryActions(args, source_select, audio_type)
        self.buildPlaylist()
        
        tools.player().play(tools.playList)
        
    def preliminaryActions(self, args, ss, at):
        self.actionArgs = json.loads(tools.unquote(args))
        self.sourceSelect = ss
        self.audioType = at
        
        tools.cancelPlayback()
        tools.playList.clear()
        
    def buildPlaylist(self):
        show = kitsu_api.KitsuBrowser().getShow(self.actionArgs['mappings']['kitsu'])
        episodes = kitsu_api.KitsuBrowser().all_episodes(self.actionArgs['mappings']['kitsu'])
        
        for a in episodes:
            if int(a['episodeNumber']) >= int(self.actionArgs['episodeNumber']):
                self.episodes.append(a)
        
        list_items = anime.List().episode_list_builder(show, self.episodes, True, self.sourceSelect, self.audioType)
        
        for a in list_items:
            tools.playList.add(url=a[0] + '&smartplay=true', listitem=a[1])
        
         