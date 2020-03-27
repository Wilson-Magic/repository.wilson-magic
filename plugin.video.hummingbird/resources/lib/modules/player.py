# -*- coding: utf-8 -*-

import json
from resources.lib.modules import tools
from resources.lib.modules import accounts

import sys
import os
import requests
    
sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])

class PlayAnime:
    def play(self, data, args):
        #Set Up Metadata
        info = json.loads(tools.unquote(args))
        
        try:
            ep_num = info['episodeNumber']
            
            genre_string = ', '.join(info['genres'])
            
            metadata = {
                'title': info['episode_title'],
                'tvshowtitle': info['titles']['canon'],
                'season': info['seasonNumber'],
                'episode': info['episodeNumber'],
                'genre': genre_string,
                'year': info['airdate'][:4],
                'plot': info['episodePlot']
            }
        except:
            genre_string = ', '.join(info['genres'])
            
            metadata = {
                'title': info['titles']['canon'],
                'genre': genre_string,
                'year': info['year'],
                'plot': info['plot']
            }       
        
        item = tools.menuItem(path=data['url'])
        item.setInfo(type='video', infoLabels=metadata)
        item.setArt(info['art'])
        item.setProperty('Video', 'true')
        item.setProperty('isPlayable', 'true')
        
        if data['adaptive'] != False and 'auengine' not in data['url']:
            item.setProperty('inputstreamaddon', 'inputstream.adaptive')
            item.setProperty('inputstream.adaptive.manifest_type', data['adaptive'])
        
        tools.setSetting('anime.lastwatched', str(info['id']))
        
        try:
            if int(info['episodeNumber']) == int(info['episode_count']):
                kitsu_status = 'completed'
                mal_status = 2
                anilist_status = 'COMPLETED'
            else:
                kitsu_status = 'current'
                mal_status = 1
                anilist_status = 'CURRENT'
        except:
            kitsu_status = 'current'
            mal_status = 1
            anilist_status = 'CURRENT'
                
        try:
            if tools.getSetting('kitsu.access') != '' and tools.getSetting('kitsu.track') == 'true':
                accounts.Kitsu().track(info['id'], info['episodeNumber'], kitsu_status)
            if tools.getSetting('mal.sessionid') != '' and tools.getSetting('mal.track') == 'true':
                accounts.Mal().track(info['id'], info['episodeNumber'], mal_status)
            if tools.getSetting('ani.userid') != '' and tools.getSetting('ani.track') == 'true':
                accounts.Anilist().track(info['id'], info['episodeNumber'], anilist_status)
        except:
            if tools.getSetting('kitsu.access') != '' and tools.getSetting('kitsu.track') == 'true':
                accounts.Kitsu().track(info['id'], '1', 'current')
            if tools.getSetting('mal.sessionid') != '' and tools.getSetting('mal.track') == 'true':
                accounts.Mal().track(info['id'], '1', 2)
            if tools.getSetting('ani.userid') != '' and tools.getSetting('ani.track') == 'true':
                accounts.Anilist().track(info['id'], '1', 'COMPLETED')
                
        tools.resolvedUrl(syshandle, True, item)
        
        if data['subtitles'] != None:
            subtitle_link = data['subtitles']
            
            sub_file_ex = subtitle_link.split('.')
            sub_file_ex = sub_file_ex[int(len(sub_file_ex)-1)]
            
            #subtitle_location = os.path.join(tools.subtitle_file, 'temp.%s' % sub_file_ex)
            subtitle_location = tools.subtitle_file

            if os.path.exists(subtitle_location):
                os.remove(subtitle_location)
            file = requests.get(subtitle_link)
            sub_data = file.text
            sub_data = sub_data.encode('utf-8')
            with open(subtitle_location, 'wb') as code:
                code.write(sub_data)
            tools.sleep(3000)
            tools.player().setSubtitles(subtitle_location)