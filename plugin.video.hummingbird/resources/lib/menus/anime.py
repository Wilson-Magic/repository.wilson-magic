# -*- coding: utf-8 -*-

import sys
import json

import datetime

from resources.lib.modules import kitsu_api
from resources.lib.modules import tools

sysaddon = sys.argv[0]
try:
    syshandle = int(sys.argv[1])
except:
    syshandle = ''

class List:
    def __init__(self):
        self.episodeList = []

    #Trending
    def trending(self):
        anime = kitsu_api.KitsuBrowser().trending()
        self.list_builder(anime)
        tools.closeDirectory('tvshows')
    
    #Top Airing
    def top_airing(self, page):
        anime = kitsu_api.KitsuBrowser().top_airing(page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'airing&page=%s' % str(page+1), None, None)
        tools.closeDirectory('tvshows')    
    
    #Top Upcoming
    def top_upcoming(self, page):
        anime = kitsu_api.KitsuBrowser().top_upcoming(page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'upcoming&page=%s' % str(page+1), None, None)
        tools.closeDirectory('tvshows')     
    
    #Most Popular
    def most_popular(self, page):
        anime = kitsu_api.KitsuBrowser().most_popular(page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'most_popular&page=%s' % (page+1), None, None)
        tools.closeDirectory('tvshows')     
    
    #Highest Rated
    def highest_rated(self, page):
        anime = kitsu_api.KitsuBrowser().highest_rated(page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'highest_rated&page=%s' % str(page+1), None, None)
        tools.closeDirectory('tvshows') 
    
    #Search
    def title_search(self, query, page):
        if query is None:
            k = tools.showKeyboard('', 'Search Anime')
            k.doModal()
            search_query = (k.getText() if k.isConfirmed() else None)
            if search_query == None or query == '':
                return
        else:
            search_query = query
        
        anime = kitsu_api.KitsuBrowser().search(title=search_query, subtype='TV,movie,ova,ona,special', page=page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'title_search&title=%s&page=%s' % (search_query, str(page+1)), None, None)
        tools.closeDirectory('tvshows')
        
    def year_list(self):
        from datetime import datetime
        year = int(datetime.today().year)
        years = []
        for a in range(1907, year + 1):
            years.append(a)
        years = sorted(years, reverse=True)
        
        #ORIGINALLY HAD MULTI SELECT FOR YEARS, DIDNT WORK EVEN THOUGH API DOCS SAID IT WOULD :S
        #tools.addDirectoryItem('Multi Select...', 'year_get', None, None)
        for a in years:
            tools.addDirectoryItem(str(a), 'year_get&year=%s' % str(a), None, None)
            
        tools.closeDirectory('addons')
        
    def year_get(self, year, page):
        if year is None:
            from datetime import datetime
            current_year = int(datetime.today().year)
            years = []
            for a in range(1907, current_year + 1):
                years.append(a)
            years = sorted(years, reverse=True)
            
            year_display_list = []
            for a in years:
                year_display_list.append(str(a))
            year_multiselect = tools.showDialog.multiselect(tools.addonName + ": Year Selection", year_display_list)
            if year_multiselect is None: return
            year_selection = []
            for selection in year_multiselect:
                year_selection.append(year_display_list[selection])
            year_string = ','.join(year_selection)
        else:
            year_string = year

        anime = kitsu_api.KitsuBrowser().search(year=year_string, page=page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'year_get&year=%s&page=%s' % (year_string, str(page+1)), None, None)
        tools.closeDirectory('tvshows')  

    def rating_list(self):
        ratings = [
            {'name': 'General Audiences', 'slug': 'G'},
            {'name': 'Parental Guidence', 'slug': 'PG'},
            {'name': 'Restricted', 'slug': 'R'}
            ]

        tools.addDirectoryItem('Multi Select...', 'rating_get', None, None)
        for a in ratings:
            tools.addDirectoryItem(a['name'], 'rating_get&rating=%s' % a['slug'], None, None)
            
        tools.closeDirectory('addons')  
    
    def rating_get(self, rating, page):
        if rating is None:    
            ratings = [
                {'name': 'General Audiences', 'slug': 'G'},
                {'name': 'Parental Guidence', 'slug': 'PG'},
                {'name': 'Restricted', 'slug': 'R'}
                ]    
            rating_display_list = []
            for a in ratings:
                rating_display_list.append(a['name'])
            rating_multiselect = tools.showDialog.multiselect(tools.addonName + ": Rating Selection", rating_display_list)
            if rating_multiselect is None: return
            rating_selection = []
            for selection in rating_multiselect:
                rating_selection.append(ratings[selection]['slug'])
            rating_string = ','.join(rating_selection)
        else:
            rating_string = rating    

        anime = kitsu_api.KitsuBrowser().search(rating=rating_string, page=page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'rating_get&rating=%s&page=%s' % (rating_string, str(page+1)), None, None)
        tools.closeDirectory('tvshows')  
        
    def season_list(self):
        seasons = [
            {'name': 'Winter', 'slug': 'winter'},
            {'name': 'Spring', 'slug': 'spring'},
            {'name': 'Summer', 'slug': 'summer'},
            {'name': 'Fall', 'slug': 'fall'}
            ]

        tools.addDirectoryItem('Multi Select...', 'season_get', None, None)
        for a in seasons:
            tools.addDirectoryItem(a['name'], 'season_get&season=%s' % a['slug'], None, None)
            
        tools.closeDirectory('addons')  
    
    def season_get(self, season, page):
        if season is None:    
            seasons = [
                {'name': 'Winter', 'slug': 'winter'},
                {'name': 'Spring', 'slug': 'spring'},
                {'name': 'Summer', 'slug': 'summer'},
                {'name': 'Fall', 'slug': 'fall'}
                ]   
            season_display_list = []
            for a in seasons:
                season_display_list.append(a['name'])
            season_multiselect = tools.showDialog.multiselect(tools.addonName + ": Season Selection", season_display_list)
            if season_multiselect is None: return
            season_selection = []
            for selection in season_multiselect:
                season_selection.append(seasons[selection]['slug'])
            season_string = ','.join(season_selection)
        else:
            season_string = season   
            
        anime = kitsu_api.KitsuBrowser().search(season=season_string, page=page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'season_get&season=%s&page=%s' % (season_string, str(page+1)), None, None)
        tools.closeDirectory('tvshows')

    def subtype_list(self):
        subtypes = [
            {'name': 'TV Shows', 'slug': 'tv'},
            {'name': 'Movies', 'slug': 'movie'},
            {'name': 'OVA', 'slug': 'ova'},
            {'name': 'ONA', 'slug': 'ona'},
            {'name': 'Specials', 'slug': 'special'}
            ]

        tools.addDirectoryItem('Multi Select...', 'subtype_get', None, None)
        for a in subtypes:
            tools.addDirectoryItem(a['name'], 'subtype_get&subtype=%s' % a['slug'], None, None)
            
        tools.closeDirectory('addons')  
    
    def subtype_get(self, subtype, page):
        if subtype is None:    
            subtypes = [
                {'name': 'TV Shows', 'slug': 'tv'},
                {'name': 'Movies', 'slug': 'movie'},
                {'name': 'OVA', 'slug': 'ova'},
                {'name': 'ONA', 'slug': 'ona'},
                {'name': 'Specials', 'slug': 'special'}
                ]   
            subtype_display_list = []
            for a in subtypes:
                subtype_display_list.append(a['name'])
            subtype_multiselect = tools.showDialog.multiselect(tools.addonName + ": Subtype Selection", subtype_display_list)
            if subtype_multiselect is None: return
            subtype_selection = []
            for selection in subtype_multiselect:
                subtype_selection.append(subtypes[selection]['slug'])
            subtype_string = ','.join(subtype_selection)
        else:
            subtype_string = subtype   
            
        anime = kitsu_api.KitsuBrowser().search(subtype=subtype_string, page=page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'subtype_get&subtype=%s&page=%s' % (subtype_string, str(page+1)), None, None)
        tools.closeDirectory('tvshows')  

    def genre_list(self):
        from resources.lib.modules import kitsu_api
        genres = kitsu_api.KitsuBrowser().all_categories()
        genres = sorted(genres, key= lambda a: (a['name']))
        
        tools.addDirectoryItem('Multi Select...', 'genre_get', None, None)
        for a in genres:
            tools.addDirectoryItem(a['name'], 'genre_get&genre=%s' % a['slug'], None, None)
            
        tools.closeDirectory('addons')

    def genre_get(self, genre, page):
        from resources.lib.modules import kitsu_api
        if genre is None:
            genres = kitsu_api.KitsuBrowser().all_categories()
            genres = sorted(genres, key= lambda a: (a['name']))
            genre_display_list = []
            for a in genres:
                genre_display_list.append(a['name'])
            genre_multiselect = tools.showDialog.multiselect(tools.addonName + ": Genre Selection", genre_display_list)
            if genre_multiselect is None: return
            genre_selection = []
            for selection in genre_multiselect:
                genre_selection.append(genres[selection]['slug'])
            genre_string = ','.join(genre_selection)
        else:
            genre_string = genre    

        anime = kitsu_api.KitsuBrowser().search(genre=genre_string, page=page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'genre_get&genre=%s&page=%s' % (genre_string, str(page+1)), None, None)
        tools.closeDirectory('tvshows')
        
    def advanced_search(self, year, rating, season, subtype, genre, page):
        items_preselect = ['Years', 'Ratings', 'Seasons', 'Subtypes', 'Genres']
        items_selected = ['Years', 'Ratings', 'Seasons', 'Subtypes', 'Genres', 'Search']
        
        years = []
        ratings = []
        seasons = []
        subtypes = []
        genres = []
        
        select = ''
        
        year_string = year
        rating_string = rating
        season_string = season
        subtype_string = subtype
        genre_string = genre
        
        if year is None and rating is None and season is None and subtype is None and genre is None:
            while select != 'Search':
                if years == [] and ratings == [] and seasons == [] and subtypes == [] and genres == []:
                    select_area = tools.showDialog.select(tools.addonName + ': Advanced Search', items_preselect)
                else:
                    select_area = tools.showDialog.select(tools.addonName + ': Advanced Search', items_selected)
                
                if select_area == -1:
                    return
                
                select = items_selected[select_area]
                
                if select == 'Years':
                    if years != []:
                        years = []
                    from datetime import datetime
                    adv_year = int(datetime.today().year)
                    adv_years = []
                    for a in range(1907, adv_year + 1):
                        adv_years.append(str(a))
                    adv_years = sorted(adv_years, reverse=True)
                    adv_select = tools.showDialog.select(tools.addonName + ': Year Selection', adv_years)
                    if adv_select is None or adv_select == -1: continue
                    years.append(adv_years[adv_select])
                    
                if select == 'Ratings':
                    if ratings != []:
                        ratings = []
                    adv_ratings = [
                        {'name': 'General Audiences', 'slug': 'G'},
                        {'name': 'Parental Guidence', 'slug': 'PG'},
                        {'name': 'Restricted', 'slug': 'R'}
                        ]    
                    rating_display_list = []
                    for a in adv_ratings:
                        rating_display_list.append(a['name'])
                    rating_multiselect = tools.showDialog.multiselect(tools.addonName + ": Rating Selection", rating_display_list)
                    if rating_multiselect is None: continue
                    rating_selection = []
                    for selection in rating_multiselect:
                        rating_selection.append(adv_ratings[selection]['slug'])
                    ratings=rating_selection

                if select == 'Seasons':
                    if seasons != []:
                        seasons = []
                    adv_seasons = [
                        {'name': 'Winter', 'slug': 'winter'},
                        {'name': 'Spring', 'slug': 'spring'},
                        {'name': 'Summer', 'slug': 'summer'},
                        {'name': 'Fall', 'slug': 'fall'}
                        ]
                    season_display_list = []
                    for a in adv_seasons:
                        season_display_list.append(a['name'])
                    season_multiselect = tools.showDialog.multiselect(tools.addonName + ": Season Selection", season_display_list)
                    if season_multiselect is None: continue
                    season_selection = []
                    for selection in season_multiselect:
                        season_selection.append(adv_seasons[selection]['slug'])
                    seasons = season_selection

                if select == 'Subtypes':
                    if subtypes != []:
                        subtypes = []
                    adv_subtypes = [
                        {'name': 'TV Shows', 'slug': 'tv'},
                        {'name': 'Movies', 'slug': 'movie'},
                        {'name': 'OVA', 'slug': 'ova'},
                        {'name': 'ONA', 'slug': 'ona'},
                        {'name': 'Specials', 'slug': 'special'}
                        ]   
                    subtype_display_list = []
                    for a in adv_subtypes:
                        subtype_display_list.append(a['name'])
                    subtype_multiselect = tools.showDialog.multiselect(tools.addonName + ": Subtype Selection", subtype_display_list)
                    if subtype_multiselect is None: continue
                    subtype_selection = []
                    for selection in subtype_multiselect:
                        subtype_selection.append(adv_subtypes[selection]['slug'])
                    subtypes = subtype_selection
                
                if select == 'Genres':
                    if genres != []:
                        genres = []
                    from resources.lib.modules import kitsu_api
                    adv_genres = kitsu_api.KitsuBrowser().all_categories()
                    adv_genres = sorted(adv_genres, key= lambda a: (a['name']))
                    genre_display_list = []
                    for a in adv_genres:
                        genre_display_list.append(a['name'])
                    genre_multiselect = tools.showDialog.multiselect(tools.addonName + ": Genre Selection", genre_display_list)
                    if genre_multiselect is None: continue
                    genre_selection = []
                    for selection in genre_multiselect:
                        genre_selection.append(adv_genres[selection]['slug'])
                    genres = genre_selection
                
            year_string = ','.join(years)
            rating_string = ','.join(ratings)
            season_string = ','.join(seasons)
            subtype_string = ','.join(subtypes)
            genre_string =  ','.join(genres)
            
        from resources.lib.modules import kitsu_api    
        anime = kitsu_api.KitsuBrowser().search(title='', year=year_string, rating=rating_string, season=season_string, subtype=subtype_string, genre=genre_string, page=page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'advanced_search&year=%s&rating=%s&season=%s&subtype=%s&genre=%s&page=%s' % (year_string, rating_string, season_string, subtype_string, genre_string, str(page+1)), None, None)
        tools.closeDirectory('tvshows')        
        
        
    def top_by_season(self, season, year, page):
        anime = kitsu_api.KitsuBrowser().search(season=season, year=year, page=page)
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'top_by_season&season=%s&year=%s&page=%s' % (season, year, str(page+1)), None, None)
        tools.closeDirectory('tvshows')  

    #Episodes
    def episode_list(self, args, page, progress):
        show_info = json.loads(tools.unquote(args))
        episodes = kitsu_api.KitsuBrowser().all_episodes(id=show_info['id'])
        self.episode_list_builder(show_info, episodes, progress)
        tools.closeDirectory('episodes')
        
    def franchise(self, args, page):
        show_info = json.loads(tools.unquote(args))
        anime = kitsu_api.KitsuBrowser().franchise(id=show_info['id'])
        self.list_builder(anime)
        if len(anime) == 20:
            tools.addDirectoryItem('Next Page...', 'franchise&page=%s' % str(page+1), None, None, actionArgs=tools.quote(tools.unquote(args)))
        tools.closeDirectory('episodes')
        
    def get_list(self, site, list):
        from resources.lib.modules import accounts
        anime = accounts.Lists().get(site, list)
        self.list_builder(anime)
        tools.closeDirectory('tvshows')
        
    def get_list_test(self, site, list):
        from resources.lib.modules import accounts_test as accounts
        anime = accounts.Lists().get(site, list)
        if site ==  'kitsu':
            self.list_builder(anime)
        else:
            self.list_builder_alt(anime, site)
        tools.closeDirectory('tvshows')
        
    def list_builder_alt(self, anime, site):
        for a in anime:
            name_choice = tools.getSetting('show.titles')
            name = a['titles']['base']
            if name_choice == 'English':
                name = a['titles']['english']
            elif name_choice == 'Kanji':
                name = a['titles']['japanese']
            
            if name is None:
                name = a['titles']['canon']
                
            if a['titles']['japanese'] is not None:
                originaltitle = a['titles']['japanese'].encode('utf-8')
            else:
                originaltitle = ''      
                
            duration = 1

            item = {'plot': a['plot'],
                    'genre': a['genres'],
                    'year': a['year'],
                    'originaltitle': originaltitle,
                    'duration': str(duration*60),
                    'country': 'Japan'}       

            if a['subtype'] == 'Movie':
                action = 'play_anime&get_anime_info=true&site=%s' % site
                folder = False
                playable = True
                cm = [('Source Select', 'PlayMedia(%s?action=play_anime&source_select=true&actionArgs=%s)' % (sysaddon, tools.quote(json.dumps(a, sort_keys=True))))]
                item['mediatype'] = 'movie'
                item['title'] = name
            else:
                action = 'episode_list&get_anime_info=true&site=%s' % site
                folder = True
                playable = False
                cm = []
                item['mediatype'] = 'tvshow'
                item['tvshowtitle'] = name
                item['status'] = a['status']

            args = tools.quote(json.dumps(a, sort_keys=True))
            
            art = {'poster': a['picture']}
 
            tools.addDirectoryItem(name, action, item, art, cm=cm, isFolder=folder, isPlayable=playable, actionArgs=args)                     
    
    #List Builder
    def list_builder(self, anime):
        for a in anime:
            name_choice = tools.getSetting('show.titles')
            name = a['titles']['canon']
            if name_choice == 'English':
                name = a['titles']['english']
            elif name_choice == 'Romaji':
                name = a['titles']['romaji']
            elif name_choice == 'Kanji':
                name = a['titles']['kanji'].encode('utf-8')
            
            if name is None:
                name = a['titles']['canon']
            
            duration = 1
            status = 'ended'
            
            try: 
                duration = int(a['episode_count'])*int(a['episode_length'])
            except: 
                try:
                    duration = int(a['episode_length'])
                except:
                    duration = 0
                
            try:
                if a['status'] == 'current':
                    status = 'returning series'
                elif a['status'] == 'finished':
                    status = 'ended'
                else:
                    status = 'in production'
            except:
                status = 'in production'

            originaltitle = ''

            if a['titles']['kanji'] is not None:
                originaltitle = a['titles']['kanji'].encode('utf-8')
            else:
                originaltitle = ''

            item = {'plot': a['plot'],
                    'genre': ', '.join(a['genres']),
                    'year': a['year'],
                    'premiered': a['start_date'],
                    'originaltitle': originaltitle,
                    'userrating': a['average_rating'],
                    'mpaa': a['age_rating'],
                    'duration': str(duration*60),
                    'country': 'Japan'}
            
            if a['subtype'] == 'movie':
                action = 'play_anime'
                folder = False
                playable = True
                cm = [('Source Select', 'PlayMedia(%s?action=play_anime&source_select=true&actionArgs=%s)' % (sysaddon, tools.quote(json.dumps(a, sort_keys=True))))]
                item['mediatype'] = 'movie'
                item['title'] = name
            else:
                action = 'episode_list'
                folder = True
                playable = False
                cm = []
                item['mediatype'] = 'tvshow'
                item['tvshowtitle'] = name
                item['status'] = status

            if 'youtube_trailer' in a:
                item['trailer'] = tools.youtube_url % a['youtube_trailer']

            args = tools.quote(json.dumps(a, sort_keys=True))
 
            tools.addDirectoryItem(name, action, item, a['art'], cm=cm, isFolder=folder, isPlayable=playable, actionArgs=args) 
            
    def episode_list_builder(self, show, episode_list, progress=False, smartPlay=False, sourceSelect=False, audioType=False):
        reverse = tools.getSetting('ep.reverse')
        shownum = tools.getSetting('ep.number')
        
        ep_list = episode_list
        
        if reverse == 'true':
            ep_list = sorted(episode_list, key=lambda x: int(x['episodeNumber']), reverse=True)
        else:
            ep_list = sorted(episode_list, key=lambda x: int(x['episodeNumber']), reverse=False)
    
        index = 0
        
        smartplay_list = []
        
        try: progress = show['account_info']['progress']
        except: progress = 0
    
        for a in ep_list:
            name_choice = tools.getSetting('ep.titles')
            name = a['episode_title']
            if name_choice == 'English':
                name = a['alt_titles']['english']
            elif name_choice == 'Romaji':
                name = a['alt_titles']['romaji']
            elif name_choice == 'Kanji':
                name = a['alt_titles']['kanji'].encode('utf-8')
                
            if name is None:
                name = 'Episode %s' % str(a['episodeNumber'])
            
            if shownum == 'true':
                name = str(a['episodeNumber']) + ' - ' + name            
                
            action = 'play_anime'
            folder = False
            playable = True
                
            if sourceSelect != False:
                action += '&source_select=true'
            if audioType != False:
                action += '&audio_type=%s' % audioType
                
            try: duration = str(show['episode_length']*60)
            except: duration = '22'
            
            item = {'plot': a['episodePlot'], 
                    'premiered': a['airdate'],
                    'year': a['year'], 
                    'mediatype': 'episode', 
                    'duration': duration,
                    'episode': int(a['episodeNumber'])}
            
            if int(a['episodeNumber']) <= progress:
                 item['playcount'] = 1
            else:
                 item['playcount'] = 0
            
            poster = a['thumbnail']
            
            if poster is None:
                poster = show['art']['poster']
            
            art = {'poster': poster,
                   'fanart': show['art']['fanart']}
            
            args = dict(show)
            args.update(a)
            
            if tools.getSetting('smartplay.enable') == 'true' and smartPlay == False:
                cm = []
            else:
                source_select_cm = ('Source Select', 'PlayMedia(%s?action=play_anime&source_select=true&actionArgs=%s)' % (sysaddon, tools.quote(json.dumps(args, sort_keys=True))))
                play_sub_cm = ('Play Subbed', 'PlayMedia(%s?action=play_anime&audio_type=bub&actionArgs=%s)' % (sysaddon, tools.quote(json.dumps(args, sort_keys=True))))
                play_dub_cm = ('Play Dubbed', 'PlayMedia(%s?action=play_anime&audio_type=sub&actionArgs=%s)' % (sysaddon, tools.quote(json.dumps(args, sort_keys=True))))
                cm = [source_select_cm, play_sub_cm, play_dub_cm]
            
            args = tools.quote(json.dumps(args, sort_keys=True))            

            smartplay_list.append(tools.addDirectoryItem(name, action, item, art, cm=cm, isFolder=folder, isPlayable=playable, actionArgs=args, bulk_add=True))
            
        if smartPlay == True:
           return smartplay_list
        else:
           tools.addMenuItems(syshandle, smartplay_list, len(smartplay_list))