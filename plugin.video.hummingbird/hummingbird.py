# -*- coding: utf-8 -*-

import sys
import os
import math
import json

from resources.lib.modules import tools

##PARAMS
params = dict(tools.parse_qsl(sys.argv[2].replace('?', '')))

action = params.get('action')
page = params.get('page')
url = params.get('url')
actionArgs = params.get('actionArgs')
source_select = params.get('source_select')
audio_type = params.get('audio_type')
smartplayCheck = params.get('smartplay')
get_kitsu_item = params.get('get_anime_info')
site = params.get('site')

if get_kitsu_item == 'true':
    get_kitsu_item = True
else:
    get_kitsu_item = False

if page is None:
    page = 1
else:
    page = int(page)
    
if source_select == 'true':
    source_select = True
else:
    source_select = False
    
if audio_type == 'sub':
    audio_type = 'Sub'
elif audio_type == 'dub':
    audio_type = 'Dub'
else:
    audio_type = None
    
if smartplayCheck == 'true':
    smart_play = True
else:
    smart_play = False
    
title = params.get('title')
year = params.get('year')
rating = params.get('rating')
season = params.get('season')
subtype = params.get('subtype')
genre = params.get('genre')

site = params.get('site')
list = params.get('list')
    
##MAIN MENU ITEMS (NOT TIED TO A R`EQUEST)
if action == None:
    from resources.lib.menus import base
    base.List().main_menu()
    
if action == 'explore_anime':
    from resources.lib.menus import base
    base.List().exploreAnime()    
    
if action == 'season':
    from resources.lib.menus import base
    base.List().season_menu()
    
if action == 'search':
    from resources.lib.menus import base
    base.List().search_menu()
    
if action == 'settings':
    tools.execute('Addon.OpenSettings(%s)' % tools.addonInfo('id'))
    
##SEARCH ITEMS
if action == 'title_search':
    from resources.lib.menus import anime
    anime.List().title_search(title, page)

if action == 'year_search':
    from resources.lib.menus import anime
    anime.List().year_list()
    
if action == 'year_get':
    from resources.lib.menus import anime
    anime.List().year_get(year, page)
    
if action == 'rating_search':
    from resources.lib.menus import anime
    anime.List().rating_list()
    
if action == 'rating_get':
    from resources.lib.menus import anime
    anime.List().rating_get(rating, page)

if action == 'season_search':
    from resources.lib.menus import anime
    anime.List().season_list()

if action == 'season_get':
    from resources.lib.menus import anime
    anime.List().season_get(season, page)

if action == 'subtype_search':
    from resources.lib.menus import anime
    anime.List().subtype_list()
    
if action == 'subtype_get':
    from resources.lib.menus import anime
    anime.List().subtype_get(subtype, page)

if action == 'genre_search':
    from resources.lib.menus import anime
    anime.List().genre_list()
    
if action == 'genre_get':
    from resources.lib.menus import anime
    anime.List().genre_get(genre, page)
    
if action == 'advanced_search':
    from resources.lib.menus import anime
    anime.List().advanced_search(year, rating, season, subtype, genre, page)
    
##OTHER MENU (TIED TO REQUESTS)
if action == 'trending':
    from resources.lib.menus import anime
    anime.List().trending()
    
if action == 'airing':
    from resources.lib.menus import anime
    anime.List().top_airing(page)
    
if action == 'upcoming':
    from resources.lib.menus import anime
    anime.List().top_upcoming(page)
    
if action == 'most_popular':
    from resources.lib.menus import anime
    anime.List().most_popular(page)
    
if action == 'highest_rated':
    from resources.lib.menus import anime
    anime.List().highest_rated(page)
    
if action == 'top_by_season':
    from resources.lib.menus import anime
    anime.List().top_by_season(season, year, page)
    
if action == 'franchise':
    from resources.lib.menus import anime
    anime.List().franchise(actionArgs, page)
    
##EPISODES STUFF    
if action == 'episode_list':
    progress_info = ''

    #Convert MAL/AniList to Kitsu item.
    if get_kitsu_item == True:
        from resources.lib.modules import accounts
        from resources.lib.modules import kitsu_api
        args = json.loads(tools.unquote(actionArgs))
        progress_info = args['account_info']
        tools.log(progress_info, 'error')
        kitsu_id = accounts.Mappings().get(site, args['id'], 'kitsu')
        extracted_info = kitsu_api.KitsuBrowser().getListById([kitsu_id], progress=progress_info)[0]
        tools.log(extracted_info, 'error')
        actionArgs = tools.quote(json.dumps(extracted_info))
    else:
        args = json.loads(tools.unquote(actionArgs))
        progress_info = args['account_info']
    
    from resources.lib.menus import anime
    anime.List().episode_list(actionArgs, page, progress_info)   
    
##PLAY
if action == 'play_anime':
    #Convert MAL/AniList to Kitsu item.
    if get_kitsu_item == True:
        from resources.lib.modules import accounts
        from resources.lib.modules import kitsu_api
        args = json.loads(tools.unquote(actionArgs))
        kitsu_id = accounts.Mappings().get(site, args['id'], 'kitsu')
        extracted_info = kitsu_api.KitsuBrowser().getListById([kitsu_id])[0]
        actionArgs = tools.quote(json.dumps(extracted_info))
    #Smartplay
    if tools.getSetting('smartplay.enable') == 'true' and smart_play == False:
        from resources.lib.modules import smartplay
        smartplay.SmartPlay().smartPlay(actionArgs, source_select, audio_type)
    else:
        tools.closeBusyDialog()    
        #Scrape
        from resources.lib.modules import sources
        animeSources = sources.GetSources().scrape(actionArgs)
        #Source Selection
        from resources.lib.modules import sourceselect
        episode_link = sourceselect.Selection().select(source_select, audio_type, animeSources)    
        if not episode_link is None:
            #Play
            from resources.lib.modules import player
            player.PlayAnime().play(episode_link, actionArgs)

##SETTINGS
if action == 'resolveurl':
    tools.addon(id="script.module.resolveurl").openSettings()
    
if action == 'iadaptive':
    tools.addon(id='inputstream.adaptive').openSettings()
    
##CACHE
if action == 'clearCache':
    from resources.lib.modules import tools
    tools.clearCache()
    
if action == 'clearDatabase':
    from resources.lib.modules import tools
    tools.clearDatabase()
    
#Accounts Stuff
if action == 'my_accounts':
    from resources.lib.menus import base
    base.List().myAccounts()
    
if action == 'my_kitsu':
    from resources.lib.menus import base
    base.List().myKitsu()
    
if action == 'my_mal':
    from resources.lib.menus import base
    base.List().myMal()
    
if action == 'my_anilist':
    from resources.lib.menus import base
    base.List().myAniList()
    
if action == 'get_list':
    from resources.lib.menus import anime
    anime.List().get_list(site, list)
    
#Test Accounts Stuff
if action == 'my_accounts_test':
    from resources.lib.menus import base
    base.List().myAccountsTest()
    
if action == 'my_kitsu_test':
    from resources.lib.menus import base
    base.List().myKitsuTest()
    
if action == 'my_mal_test':
    from resources.lib.menus import base
    base.List().myMalTest()
    
if action == 'my_anilist_test':
    from resources.lib.menus import base
    base.List().myAniListTest()
    
if action == 'get_list_test':
    from resources.lib.menus import anime
    anime.List().get_list_test(site, list)
    
#Login
if action == 'kitsuLogin':
    from resources.lib.modules import accounts
    accounts.Kitsu().login()
    
if action == 'malLogin':
    from resources.lib.modules import accounts
    accounts.Mal().login()
    
if action == 'anilistLogin':
    from resources.lib.modules import accounts
    accounts.Anilist().login()
    
#Admin Commands
if action == 'adminCommands':
    if tools.getSetting('admin.warning') == 'false':
        warning = tools.showDialog.yesno(tools.addonName, 'These commands enable features that are not enabled by default FOR A REASON, they will not break the addon but are only recommended for certain audiences', yeslabel='OK', nolabel="OK - Don't Show Again")
        if warning == False:
            tools.setSetting('admin.warning', 'true')  
    k = tools.showKeyboard('', 'Admin Commands')
    k.doModal()
    command = (k.getText() if k.isConfirmed() else None)
    if command == None:
        tools.showDialog.notification(tools.addonName, 'No command entered.')
    elif command == 'degenerate':
        tools.setSetting('kitsu.18plus', 'true')
        tools.showDialog.ok(tools.addonName, 'You can now view 18+ content if signed into Kitsu.')