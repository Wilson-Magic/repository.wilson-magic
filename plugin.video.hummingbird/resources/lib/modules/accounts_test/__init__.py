from . import anilist, kitsu, myanimelist, track

Kitsu = kitsu.List()
Mal = myanimelist.List()
Anilist = anilist.List()
#Track = track.Track()

class Lists:
    def get(self, site, list):
        if site == 'kitsu' and list == 'current':
            anime = Kitsu.getCurrent()
        elif site == 'kitsu' and list == 'finished':
            anime = Kitsu.getFinished()
        elif site == 'kitsu' and list == 'dropped':
            anime = Kitsu.getDropped()
        elif site == 'kitsu' and list == 'on_hold':
            anime = Kitsu.getHold()
        elif site == 'kitsu' and list == 'planned':
            anime = Kitsu.getPlanned()        
        
        elif site == 'mal' and list == 'current':
            anime = Mal.getCurrent()
        elif site == 'mal' and list == 'finished':
            anime = Mal.getFinished()
        elif site == 'mal' and list == 'dropped':
            anime = Mal.getDropped()        
        elif site == 'mal' and list == 'on_hold':
            anime = Mal.getHold()
        elif site == 'mal' and list == 'planned':
            anime = Mal.getPlanned() 
        
        elif site == 'anilist' and list == 'current':
            anime = Anilist.getCurrent()
        elif site == 'anilist' and list == 'finished':
            anime = Anilist.getFinished()
        elif site == 'anilist' and list == 'dropped':
            anime = Anilist.getDropped()
        elif site == 'anilist' and list == 'on_hold':
            anime = Anilist.getHold()
        elif site == 'anilist' and list == 'planned':
            anime = Anilist.getPlanned() 
            
        return anime
        
    def track(self, site, id, episode, status):
        if site == 'kitsu':
            Track.kitsu(id, episode, status)
        elif site == 'mal':
            Track.myanimelist(id, episode, status)
        elif site == 'anilist':
            Track.anilist(id, episode, status)