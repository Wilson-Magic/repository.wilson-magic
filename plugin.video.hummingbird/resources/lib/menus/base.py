# -*- coding: utf-8 -*-

import sys
import os
import json
from resources.lib.modules import tools
from resources.lib.modules import kitsu_api

class List:   
    def __init__(self):
        self.kitsu_access = tools.getSetting('kitsu.access')
        self.kitsu_user = tools.getSetting('kitsu.user')
        self.mal_access = tools.getSetting('mal.sessionid')
        self.mal_user = tools.getSetting('mal.user')
        self.ani_access = tools.getSetting('ani.userid')
        self.ani_user = tools.getSetting('ani.user')
        
        self.last_watched = tools.getSetting('anime.lastwatched')
    
    def main_menu(self):
        if self.last_watched:
            self.add_last_watched()
        if self.kitsu_access or self.mal_access or self.ani_access:
            tools.addDirectoryItem('My Accounts', 'my_accounts_test', {'plot': 'Explore your account lists from Kitsu, MyAnimeList and AniList.', 'description': 'Explore your account lists from Kitsu, MyAnimeList and AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'account.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})                
        tools.addDirectoryItem('Explore Anime...', 'explore_anime', {'plot': 'Explore anime on Kitsu.', 'description': 'Explore anime on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'explore_anime.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Search', 'title_search', {'plot': 'Search anime by title on Kitsu.', 'description': 'Search anime by title on Kitsu.'}, {'poster': os.path.join(tools.OTHER_PATH, 'search.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Advanced Search', 'advanced_search', {'plot': 'Search anime on Kitsu.', 'description': 'Search anime on Kitsu.'}, {'poster': os.path.join(tools.OTHER_PATH, 'advanced_search.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Settings', 'settings', {'plot': 'Adjust the settings.', 'description': 'Adjust the settings.'}, {'poster': os.path.join(tools.OTHER_PATH, 'settings.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})

        tools.closeDirectory('tvshows')

    def exploreAnime(self):
        tools.addDirectoryItem('Trending', 'trending', {'plot': 'Explore trending anime on Kitsu.', 'description': 'Explore trending anime on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'trending.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Currently Airing', 'airing', {'plot': 'Explore currently airing anime on Kitsu.', 'description': 'Explore currently airing anime on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'currently_airing.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Upcoming', 'upcoming', {'plot': 'Explore upcoming anime on Kitsu.', 'description': 'Explore upcoming anime on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'upcoming.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Most Popular', 'most_popular', {'plot': 'Explore the most popular anime on Kitsu.', 'description': 'Explore the most popular anime on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'most_popular.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Highest Rated', 'highest_rated', {'plot': 'Explore the highest rated anime on Kitsu.', 'description': 'Explore the highest rated anime on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'highest_rated.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('By Season', 'season', {'plot': 'Explore anime by specific season on Kitsu.', 'description': 'Explore anime by specific season on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'by_season.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Genres', 'genre_search', {'plot': 'Explore anime by genre on Kitsu.', 'description': 'Explore anime by genre on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'genres.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Years', 'year_search', {'plot': 'Explore anime by year on Kitsu.', 'description': 'Explore anime by year on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'years.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Subtypes', 'subtype_search', {'plot': 'Explore anime by subtype on Kitsu.', 'description': 'Explore anime by subtype on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'subtypes.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})        
        tools.addDirectoryItem('Seasons', 'season_search', {'plot': 'Explore anime by seasons on Kitsu.', 'description': 'Explore anime by seasons on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'seasons.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Ratings', 'rating_search', {'plot': 'Explore anime by age ratings on Kitsu.', 'description': 'Explore anime by age ratings on Kitsu.'}, {'poster': os.path.join(tools.BASIC_PATH, 'ratings.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.closeDirectory('tvshows')          
        
    def myAccounts(self):
        if self.kitsu_access:
            tools.addDirectoryItem('My Kitsu - %s' % self.kitsu_user, 'my_kitsu', {'plot': 'Explore your lists on Kitsu.', 'description': 'Explore your lists on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        if self.mal_access:
            tools.addDirectoryItem('My MAL - %s' % self.mal_user, 'my_mal', {'plot': 'Explore your lists on MyAnimeList.', 'description': 'Explore your lists on MyAnimeList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        if self.ani_access:
            tools.addDirectoryItem('My AniList - %s' % self.ani_user, 'my_anilist', {'plot': 'Explore your lists on AniList.', 'description': 'Explore your lists on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.closeDirectory('tvshows')
        
    def myKitsu(self):
        tools.addDirectoryItem('Currently Watching', 'get_list&site=kitsu&list=current', {'plot': 'Explore currently watching anime on Kitsu.', 'description': 'Explore currently watching on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Finished', 'get_list&site=kitsu&list=finished', {'plot': 'Explore finished anime on Kitsu.', 'description': 'Explore finished on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Dropped', 'get_list&site=kitsu&list=dropped', {'plot': 'Explore dropped anime on Kitsu.', 'description': 'Explore dropped on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('On Hold', 'get_list&site=kitsu&list=on_hold', {'plot': 'Explore on hold anime on Kitsu.', 'description': 'Explore on hold on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Planned', 'get_list&site=kitsu&list=planned', {'plot': 'Explore planned anime on Kitsu.', 'description': 'Explore currently watching on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.closeDirectory('tvshows')

    def myMal(self):
        tools.addDirectoryItem('Currently Watching', 'get_list&site=mal&list=current', {'plot': 'Explore currently watching anime on MyAnimeList.', 'description': 'Explore currently watching anime on MyAnimeList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Finished', 'get_list&site=mal&list=finished', {'plot': 'Explore finished anime on MyAnimeList.', 'description': 'Explore finished anime on MyAnimeList'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Dropped', 'get_list&site=mal&list=dropped', {'plot': 'Explore dropped anime on MyAnimeList.', 'description': 'Explore dropped anime on MyAnimeList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('On Hold', 'get_list&site=mal&list=on_hold', {'plot': 'Explore on hold anime on MyAnimeList.', 'description': 'Explore on hold anime on MyAnimeList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Planned', 'get_list&site=mal&list=planned', {'plot': 'Explore planned anime on MyAnimeList.', 'description': 'Explore planned anime on MyAnimeList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.closeDirectory('tvshows')
        
    def myAniList(self):
        tools.addDirectoryItem('Currently Watching', 'get_list&site=anilist&list=current', {'plot': 'Explore currently watching anime on AniList.', 'description': 'Explore currently watching anime on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Finished', 'get_list&site=anilist&list=finished', {'plot': 'Explore finished anime on AniList.', 'description': 'Explore finished anime on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Dropped', 'get_list&site=anilist&list=dropped', {'plot': 'Explore dropped anime on AniList.', 'description': 'Explore dropped anime on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('On Hold', 'get_list&site=anilist&list=on_hold', {'plot': 'Explore on hold anime on AniList.', 'description': 'Explore on hold anime on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Planned', 'get_list&site=anilist&list=planned', {'plot': 'Explore planned anime on AniList.', 'description': 'Explore planned anime on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.closeDirectory('tvshows')
        
    def season_menu(self):
        from datetime import datetime
        
        year = int(datetime.today().year)
        month = int(datetime.today().month)
        day = int(datetime.today().day)
        
        if month == 1 or month == 2 or month == 3:
            season = 'Winter'
        elif month == 4 or month == 5 or month == 6:
            season = 'Spring'
        elif month == 7 or month == 8 or month == 9:
            season = 'Summer'
        elif month == 10 or month == 11 or month == 12:
            season = 'Fall'
            
        dec_seasons = ['Fall', 'Summer', 'Spring', 'Winter']
        
        seasons_so_far = []
        
        if season == 'Winter':
            seasons_so_far.append('Winter')
        elif season == 'Spring':
            seasons_so_far.append('Spring')
            seasons_so_far.append('Winter')
        elif season == 'Summer':
            seasons_so_far.append('Summer')
            seasons_so_far.append('Spring')
            seasons_so_far.append('Winter')
        elif season == 'Fall':
            seasons_so_far.append('Fall')
            seasons_so_far.append('Summer')
            seasons_so_far.append('Spring')
            seasons_so_far.append('Winter')
        
        years = []      
        
        for i in range(1980, year):
            years.append(i)
        years = sorted(years, reverse=True)
            
        for a in seasons_so_far:
            meme_material = {'plot': 'Explore anime from %s %s.' % (a, year), 'description': 'Explore anime from %s %s.' % (a, year)}
            tools.addDirectoryItem('%s %s' % (a, year), 'top_by_season&season=%s&year=%s' % (a.lower(), year), meme_material, None)
            
        for a in years:
            for b in dec_seasons:
                meme_material = {'plot': 'Explore anime from %s %s.' % (b, a), 'description': 'Explore anime from %s %s.' % (b, a)}
                tools.addDirectoryItem('%s %s' % (b, a), 'top_by_season&season=%s&year=%s' % (b.lower(), a), meme_material, None)
            
        tools.closeDirectory('tvshows')        
               
    def add_last_watched(self):
        a = kitsu_api.KitsuBrowser().getShow(self.last_watched)
        
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
            
        name = 'Last Watched: %s' % name
        
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
            cm = []
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
        
#################################TESTS##################################
    def myAccountsTest(self):
        if self.kitsu_access:
            tools.addDirectoryItem('My Kitsu - %s' % self.kitsu_user, 'my_kitsu_test', {'plot': 'Explore your lists on Kitsu.', 'description': 'Explore your lists on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        if self.mal_access:
            tools.addDirectoryItem('My MAL - %s' % self.mal_user, 'my_mal_test', {'plot': 'Explore your lists on MyAnimeList.', 'description': 'Explore your lists on MyAnimeList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        if self.ani_access:
            tools.addDirectoryItem('My AniList - %s' % self.ani_user, 'my_anilist_test', {'plot': 'Explore your lists on AniList.', 'description': 'Explore your lists on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.closeDirectory('tvshows')    
        
        
    def myKitsuTest(self):
        tools.addDirectoryItem('Currently Watching', 'get_list_test&site=kitsu&list=current', {'plot': 'Explore currently watching anime on Kitsu.', 'description': 'Explore currently watching on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Finished', 'get_list_test&site=kitsu&list=finished', {'plot': 'Explore finished anime on Kitsu.', 'description': 'Explore finished on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Dropped', 'get_list_test&site=kitsu&list=dropped', {'plot': 'Explore dropped anime on Kitsu.', 'description': 'Explore dropped on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('On Hold', 'get_list_test&site=kitsu&list=on_hold', {'plot': 'Explore on hold anime on Kitsu.', 'description': 'Explore on hold on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Planned', 'get_list_test&site=kitsu&list=planned', {'plot': 'Explore planned anime on Kitsu.', 'description': 'Explore currently watching on Kitsu.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'kitsu.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.closeDirectory('tvshows')

    def myMalTest(self):
        tools.addDirectoryItem('Currently Watching', 'get_list_test&site=mal&list=current', {'plot': 'Explore currently watching anime on MyAnimeList.', 'description': 'Explore currently watching anime on MyAnimeList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Finished', 'get_list_test&site=mal&list=finished', {'plot': 'Explore finished anime on MyAnimeList.', 'description': 'Explore finished anime on MyAnimeList'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Dropped', 'get_list_test&site=mal&list=dropped', {'plot': 'Explore dropped anime on MyAnimeList.', 'description': 'Explore dropped anime on MyAnimeList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('On Hold', 'get_list_test&site=mal&list=on_hold', {'plot': 'Explore on hold anime on MyAnimeList.', 'description': 'Explore on hold anime on MyAnimeList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Planned', 'get_list_test&site=mal&list=planned', {'plot': 'Explore planned anime on MyAnimeList.', 'description': 'Explore planned anime on MyAnimeList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'mal.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.closeDirectory('tvshows')
        
    def myAniListTest(self):
        tools.addDirectoryItem('Currently Watching', 'get_list_test&site=anilist&list=current', {'plot': 'Explore currently watching anime on AniList.', 'description': 'Explore currently watching anime on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Finished', 'get_list_test&site=anilist&list=finished', {'plot': 'Explore finished anime on AniList.', 'description': 'Explore finished anime on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Dropped', 'get_list_test&site=anilist&list=dropped', {'plot': 'Explore dropped anime on AniList.', 'description': 'Explore dropped anime on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('On Hold', 'get_list_test&site=anilist&list=on_hold', {'plot': 'Explore on hold anime on AniList.', 'description': 'Explore on hold anime on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.addDirectoryItem('Planned', 'get_list_test&site=anilist&list=planned', {'plot': 'Explore planned anime on AniList.', 'description': 'Explore planned anime on AniList.'}, {'poster': os.path.join(tools.ACCOUNTS_PATH, 'anilist.png'), 'fanart': os.path.join(tools.MEDIA_PATH, 'fanart.jpg')})
        tools.closeDirectory('tvshows')