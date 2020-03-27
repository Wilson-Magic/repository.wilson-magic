# -*- coding: utf-8 -*-
# This is a remnant from when this was originally much closer to the Seren fork it started off as, so this is holdover from that.
# <3 Seren

import requests
import json
import os
import sys
import threading
import unicodedata
import re
import datetime
# Import _strptime to workaround python 2 bug with threads
import _strptime
import time
import ast

try:
    from urlparse import parse_qsl, parse_qs, unquote, urlparse
    from urllib import urlencode, quote_plus, quote
except:
    from urllib.parse import parse_qsl, urlencode, quote_plus, parse_qs, quote, unquote, urlparse

try:
    sysaddon = sys.argv[0]
    syshandle = int(sys.argv[1])
except:
    sysaddon = ''
    syshandle = '1'
    pass

tmdb_semaphore = 40

tmdb_sema = threading.Semaphore(tmdb_semaphore)

database_sema = threading.Semaphore(1)

tv_semaphore = 100

tv_sema = threading.Semaphore(tv_semaphore)

tvdb_refreshing = False

tvdb_refresh = ''

viewTypes = {
    'List': 50,
    'Poster': 51,
    'Icon Wall': 52,
    'Shift': 53,
    'Info Wall': 54,
    'Wide List': 55,
    'Wall': 500,
    'Banner': 501,
    'Fanart': 502,
}

colorChart = ['black', 'white', 'whitesmoke', 'gainsboro', 'lightgray', 'silver', 'darkgray', 'gray', 'dimgray',
              'snow', 'floralwhite', 'ivory', 'beige', 'cornsilk', 'antiquewhite', 'bisque', 'blanchedalmond',
              'burlywood', 'darkgoldenrod', 'ghostwhite', 'azure', 'aliveblue', 'lightsaltegray', 'lightsteelblue',
              'powderblue', 'lightblue', 'skyblue', 'lightskyblue', 'deepskyblue', 'dodgerblue', 'royalblue',
              'blue', 'mediumblue', 'midnightblue', 'navy', 'darkblue', 'cornflowerblue', 'slateblue', 'slategray',
              'yellowgreen', 'springgreen', 'seagreen', 'steelblue', 'teal', 'fuchsia', 'deeppink', 'darkmagenta',
              'blueviolet', 'darkviolet', 'darkorchid', 'darkslateblue', 'darkslategray', 'indigo', 'cadetblue',
              'darkcyan', 'darkturquoise', 'turquoise', 'cyan', 'paleturquoise', 'lightcyan', 'mintcream', 'honeydew',
              'aqua', 'aquamarine', 'chartreuse', 'greenyellow', 'palegreen', 'lawngreen', 'lightgreen', 'lime',
              'mediumspringgreen', 'mediumturquoise', 'lightseagreen', 'mediumaquamarine', 'mediumseagreen',
              'limegreen', 'darkseagreen', 'forestgreen', 'green', 'darkgreen', 'darkolivegreen', 'olive', 'olivedab',
              'darkkhaki', 'khaki', 'gold', 'goldenrod', 'lightyellow', 'lightgoldenrodyellow', 'lemonchiffon',
              'yellow', 'seashell', 'lavenderblush', 'lavender', 'lightcoral', 'indianred', 'darksalmon',
              'lightsalmon', 'pink', 'lightpink', 'hotpink', 'magenta', 'plum', 'violet', 'orchid', 'palevioletred',
              'mediumvioletred', 'purple', 'marron', 'mediumorchid', 'mediumpurple', 'mediumslateblue', 'thistle',
              'linen', 'mistyrose', 'palegoldenrod', 'oldlace', 'papayawhip', 'moccasin', 'navajowhite', 'peachpuff',
              'sandybrown', 'peru', 'chocolate', 'orange', 'darkorange', 'tomato', 'orangered', 'red', 'crimson',
              'salmon', 'coral', 'firebrick', 'brown', 'darkred', 'tan', 'rosybrown', 'sienna', 'saddlebrown']

BROWSER_AGENTS = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
    
season_identifiers = {
    '1': ['1', 'Season 1', '1st Season'],
    '2': ['2', 'Season 2', '2nd Season'],
    '3': ['3', 'Season 3', '3rd Season'],
    '4': ['4', 'Season 4', '4th Season'],
    '5': ['5', 'Season 5', '5th Season'],
    '6': ['6', 'Season 6', '6th Season'],
    '7': ['7', 'Season 7', '7th Season'], 
    '8': ['8', 'Season 8', '8th Season'],
    '9': ['9', 'Season 9', '9th Season'],
    '10': ['10', 'Season 10', '10th Season']
}

menu_sort = {
    'Popularity': 'popularityRank',
    '-Popularity': '-popularityRank',
    'Rating': 'ratingRank',
    '-Rating': '-ratingRank',
    'Date': 'startDate',
    '-Date': '-startDate'
    }
    
account_sort = {
    'kitsu': {
        'Update Date': '-progressed_at',
        '-Update Date': 'progressed_at',
        'Progress': '-progress',
        '-Progress': 'progress',
        'Alphabetical': 'anime.titles.canonical'
        },
    'mal': {
        'Update Date': 'order=5&status=%s',
        '-Update Date': 'order=5&status=%s',
        'Progress': 'order=12&status=%s',
        '-Progress': 'order=12&status=%s',
        'Alphabetical': 'order=1&status=%s'
        },
    'anilist': {
        'Update Date': 'UPDATED_TIME',
        '-Update Date': 'UPDATED_TIME',
        'Progress': 'PROGRESS',
        '-Progress': 'PROGRESS',
        'Alphabetical': 'UPDATED_TIME'
        }
    }

addonName = "Hummingbird"

import xbmcaddon, xbmc, xbmcgui, xbmcplugin, xbmcvfs

addonInfo = xbmcaddon.Addon().getAddonInfo

# GLOBAL VARIABLES
try:
    ADDON_PATH = xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
except:
    ADDON_PATH = xbmcaddon.Addon().getAddonInfo('path')

MEDIA_PATH = os.path.join(ADDON_PATH, 'resources', 'media')
SCREENSHOT_PATH = os.path.join(MEDIA_PATH, 'screenshots')
MENU_PATH = os.path.join(MEDIA_PATH, 'menus')
ACCOUNTS_PATH = os.path.join(MENU_PATH, 'accounts')
BASIC_PATH = os.path.join(MENU_PATH, 'basic')
OTHER_PATH = os.path.join(MENU_PATH, 'other')

XBFONT_LEFT = 0x00000000
XBFONT_RIGHT = 0x00000001
XBFONT_CENTER_X = 0x00000002
XBFONT_CENTER_Y = 0x00000004
XBFONT_TRUNCATED = 0x00000008
imageControl = xbmcgui.ControlImage
labelControl = xbmcgui.ControlLabel
buttonControl = xbmcgui.ControlButton
istControl = xbmcgui.ControlList
multi_text = xbmcgui.ControlTextBox

addonDir = os.path.join(xbmc.translatePath('special://home'), 'addons/plugin.video.%s' % addonName.lower())

try:
    dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')
except:
    dataPath = xbmc.translatePath(addonInfo('profile'))

subtitle_file = os.path.join(dataPath, 'temp_subs.sub')

SETTINGS_PATH = os.path.join(dataPath, 'settings.xml')

cacheFile = os.path.join(dataPath, 'cache.db')

databaseFile = os.path.join(dataPath, 'database.db')

torrentScrapeCacheFile = os.path.join(dataPath, 'torrentScrape.db')

activeTorrentsDBFile = os.path.join(dataPath, 'activeTorrents.db')

providersDB = os.path.join(dataPath, 'providers.db')

premiumizeDB = os.path.join(dataPath, 'premiumize.db')

traktSyncDB = os.path.join(dataPath, 'traktSync.db')

searchHistoryDB = os.path.join(dataPath, 'search.db')

kodiVersion = int(xbmc.getInfoLabel("System.BuildVersion")[:2])

openFile = xbmcvfs.File

makeFile = xbmcvfs.mkdir

deleteFile = xbmcvfs.delete

deleteDir = xbmcvfs.rmdir

listDir = xbmcvfs.listdir

execute = xbmc.executebuiltin

console_mode = False

youtube_url = 'plugin://plugin.video.youtube/play/?video_id=%s'

kodiGui = xbmcgui

kodi = xbmc

language = xbmc.getLanguage()

dialogWindow = kodiGui.WindowDialog

addon = xbmcaddon.Addon

progressDialog = xbmcgui.DialogProgress()

bgProgressDialog = xbmcgui.DialogProgressBG

showDialog = xbmcgui.Dialog()

endDirectory = xbmcplugin.endOfDirectory

condVisibility = xbmc.getCondVisibility

getLangString = xbmcaddon.Addon().getLocalizedString

addMenuItem = xbmcplugin.addDirectoryItem

addMenuItems = xbmcplugin.addDirectoryItems

menuItem = xbmcgui.ListItem

langString = xbmcaddon.Addon().getLocalizedString

content = xbmcplugin.setContent

resolvedUrl = xbmcplugin.setResolvedUrl

showKeyboard = xbmc.Keyboard

fileBrowser = showDialog.browse

sortMethod = xbmcplugin.addSortMethod

playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

player = xbmc.Player

def get_kitsu_streaming_links(id):
    resp = requests.get('https://kitsu.io/api/edge/anime/%s/streaming-links' % id, headers={'Accept': 'application/vnd.api+json', 'Content-Type': 'application/vnd.api+json'})
    load = json.loads(resp.content)
    data = load['data']
    
    links = {}
    
    for a in data:
        info = re.findall(r'\.(.*)\..*\/(.*)', a['attributes']['url'])[0]
        links[info[0]] = info[1]    
    
    return links

def cancelPlayback():
    playList.clear()
    resolvedUrl(syshandle, False, menuItem())
    closeOkDialog()

def get_season_number(titles):
    title_types = ['canon', 'english', 'romaji']
    
    season = 1
    
    for a in title_types:
        for b in season_identifiers:
            for c in season_identifiers[b]:
                if c in titles[a]:
                    season = int(b)
                        
    return season

def get_franchise_name(titles):
    title_types = ['canon', 'english', 'romaji']
    
    title = {}
    
    for a in title_types:
        for b in season_identifiers:
            for c in season_identifiers[b]:
                if c in titles[a]:
                    title[a] = titles[a].replace(' ' + str(c), '')
                
    if title == {}:
        title = titles
                
    return title
    
def checkLoginStatus():
    kitsu_user = getSetting('kitsu.userid')
    mal_user = getSetting('mal.sessionid')
    anilist_user = getSetting('ani.userid')
    
    loggedIn = False
    
    if kitsu_user != '' or kitsu_user != None:
        loggedIn = True
    if mal_user != '' or mal_user != None:
        loggedIn = True
    if anilist_user != '' or anilist_user != None:
        loggedIn = True
        
    return loggedIn

def get_random_ua():
    import random
    return random.choice(BROWSER_AGENTS)

def lang(language_id):
    text = getLangString(language_id)
    text = text.encode('utf-8', 'replace')
    text = display_string(text)
    return text

def addDirectoryItem(name, query, info, art, cm=[], isPlayable=False, isAction=True, isFolder=True,
                     actionArgs=False, set_cast=False, label2=None, set_ids=None, bulk_add=False):

    url = '%s?action=%s' % (sysaddon, query) if isAction else query
    if actionArgs is not False:
        url += '&actionArgs=%s' % actionArgs
    item = menuItem(label=name)
    if label2 is not None:
        item.setLabel2(label2)
    if isPlayable:
        item.setProperty('IsPlayable', 'true')
    else:
        item.setProperty('IsPlayable', 'false')
    try:
        if 'UnWatchedEpisodes' in info:
            item.setProperty('UnWatchedEpisodes', str(info['UnWatchedEpisodes']))
        if 'episodeCount' in info:
            item.setProperty('TotalEpisodes', str(info['episodeCount']))
        if 'WatchedEpisodes' in info:
            item.setProperty('WatchedEpisodes', str(info['WatchedEpisodes']))
    except:
        pass

    if set_cast is not False:
        item.setCast(set_cast)
    if set_ids is not None:
        item.setUniqueIDs(set_ids)

    item.addContextMenuItems(cm)
    
    if art == None:
        art = {'poster': os.path.join(MEDIA_PATH, 'icon.png'), 'fanart': os.path.join(MEDIA_PATH, 'fanart.jpg')}
    item.setArt(art)

    info = clean_info_keys(info)
    item.setInfo('video', info)

    if bulk_add:
        return (url, item, isFolder)
    else:
        addMenuItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

def clean_info_keys(info_dict):

    keys_to_pop = ['UnwatchedEpisodes', 'episode_count', 'unwatchedepisodes', 'WatchedEpisodes',
                   'seasonCount', 'episodeCount', 'showaliases', 'absoluteNumber']

    for i in keys_to_pop:
        try:
            info_dict.pop(i, None)
        except:
            pass

    return info_dict

def sleep(ms):
    xbmc.sleep(ms)

def closeDirectory(contentType, sort=False):
    if sort == 'title':
        sortMethod(syshandle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    if sort == 'episode':
        sortMethod(syshandle, xbmcplugin.SORT_METHOD_EPISODE)
    if not sort:
        sortMethod(syshandle, xbmcplugin.SORT_METHOD_NONE)

    viewType = get_view_type(contentType)

    content(syshandle, contentType)

    endDirectory(syshandle)
    xbmc.sleep(200)

    #if getSetting('general.setViews') == 'true':
    xbmc.executebuiltin('Container.SetViewMode(%s)' % str(viewType))


def get_view_type(contentType):
    viewType = 'Wide List'

    try:
        if contentType == 'addons':
            viewType = getSetting('main.viewtype')
        if contentType == 'tvshows':
            viewType = getSetting('show.viewtype')
        if contentType == 'episodes':
            viewType = getSetting('ep.viewtype')        
            
        #if contentType == 'tvshows':
            #viewType = getSetting('show.view')
        #if contentType == 'movies':
            #viewType = getSetting('movie.view')
        #if contentType == 'episodes':
            #viewType = getSetting('episode.view')
        #if contentType == 'seasons':
            #viewType = getSetting('season.view')

        viewType = viewTypes[viewType]

        #if getSetting('general.viewidswitch') == 'true':
            #if contentType == 'tvshows':
                #viewType = getSetting('show.view.id')
            #if contentType == 'movies':
                #viewType = getSetting('movie.view.id')
            #if contentType == 'episodes':
                #viewType = getSetting('episode.view.id')
            #if contentType == 'seasons':
                #viewType = getSetting('season.view.id')

        viewType = int(viewType)
    except:
        pass

    #log('VIEWTYPE: %s - %s' % (contentType, viewType), 'error')

    return viewType


def closeOkDialog():
    execute('Dialog.Close(okdialog, true)')


def closeBusyDialog():
    if condVisibility('Window.IsActive(busydialog)'):
        execute('Dialog.Close(busydialog)')
    if condVisibility('Window.IsActive(busydialognocancel)'):
        execute('Dialog.Close(busydialognocancel)')


def safeStr(obj):
    try:
        return str(obj)
    except UnicodeEncodeError:
        return obj.encode('utf-8', 'ignore').decode('ascii', 'ignore')
    except:
        return ""


def log(msg, level='info'):
    msg = safeStr(msg)
    msg = addonName.upper() + ': ' + msg
    if level == 'error':
        xbmc.log(msg, level=xbmc.LOGERROR)
    elif level == 'info':
        xbmc.log(msg, level=xbmc.LOGINFO)
    elif level == 'notice':
        xbmc.log(msg, level=xbmc.LOGNOTICE)
    elif level == 'warning':
        xbmc.log(msg, level=xbmc.LOGWARNING)
    else:
        xbmc.log(msg)


def colorPicker():
    selectList = []
    for i in colorChart:
        selectList.append(colorString(i, i))
    color = showDialog.select(addonName + lang(32021), selectList)
    if color == -1:
        return
    setSetting('general.textColor', colorChart[color])
    setSetting('general.displayColor', colorChart[color])


def deaccentString(text):
    text = u'%s' % text
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text


def colorString(text, color=None):

    if type(text) is not int:
       text = display_string(text)

    if color is 'default' or color is '' or color is None:
        color = getSetting('general.textColor')
        if color is '':
            color = 'deepskyblue'

    return '[COLOR %s]%s[/COLOR]' % (color, text)


def display_string(object):

    if type(object) is str or type(object) is unicode:
        return deaccentString(object)
    if type(object) is int:
        return '%s' % object
    if type(object) is bytes:
        object = ''.join(chr(x) for x in object)
        return object


def sort_list_items(threadList, originalList):
    sortedList = []

    for o in originalList:
        if o is None:
            continue
        for t in threadList:
            if t is not None:
                if 'ids' in t:
                    if t['ids']['trakt'] == o['ids']['trakt']:
                        sortedList.append(t)
                else:
                    continue
            else:
                continue
    return sortedList


def sort_anime_by_json(given_list, original_list):
    sorted_list = []
    
    for a in original_list:
        original_id = a['id']
        for b in given_list:
            given_id = b['mappings']['kitsu']
            if original_id == given_id:
                sorted_list.append(b)
    
    return sorted_list
    
def sort_anime_by_id(given_list, original_list):
    sorted_list = []
    
    for a in original_list:
        log(a, 'error')
        original_id = a
        for b in given_list:
            log(b, 'error')
            given_id = b['mappings']['kitsu']
            if original_id == given_id:
                sorted_list.append(b)
    
    log(sorted_list, 'error')
    return sorted_list
    
def metaFile():
    return os.path.join(xbmcaddon.Addon('plugin.video.%s' % addonName.lower()).getAddonInfo('path'), 'resources',
                        'cache', 'meta.db')


def clearCache():
    confirm = showDialog.yesno(addonName, 'Are you sure you want to clear the cache?')
    if confirm is 1:
        from resources.lib.modules import cache
        cache.cacheLib().clear()
        log(addonName + ': Cache Cleared', 'debug')
    else:
        pass

def clearDatabase():
    confirm = showDialog.yesno(addonName, 'Are you sure you want to clear the database?')
    if confirm is 1:
        from resources.lib.modules.Hummingbird.lib import database
        database.cacheLib().clear()
        log(addonName + ': Database Cleared', 'debug')
    else:
        pass

def returnUrl(item):
    return quote_plus(json.dumps(item))


def remove_duplicate_dicts(src_lst, ignored_keys):
    filtered = {tuple((k, d[k]) for k in sorted(d) if k not in ignored_keys): d for d in src_lst}
    dst_lst = list(filtered.values())
    return dst_lst


import subprocess


def copy2clip(txt):
    platform = sys.platform

    if platform == 'win32':
        try:
            cmd = 'echo ' + txt.strip() + '|clip'
            return subprocess.check_call(cmd, shell=True)
            pass
        except:
            pass
    elif platform == 'linux2':
        try:
            from subprocess import Popen, PIPE

            p = Popen(['xsel', '-pi'], stdin=PIPE)
            p.communicate(input=txt)
        except:
            pass
    else:
        pass
    pass


EPOCH_DATETIME = datetime.datetime(1970, 1, 1)
SECONDS_PER_DAY = 24 * 60 * 60


def utc_to_local_datetime(utc_datetime):
    delta = utc_datetime - EPOCH_DATETIME
    utc_epoch = SECONDS_PER_DAY * delta.days + delta.seconds
    if getSetting('general.datedelay') == 'true':
        utc_epoch += SECONDS_PER_DAY
    time_struct = time.localtime(utc_epoch)
    dt_args = time_struct[:6] + (delta.microseconds,)
    return datetime.datetime(*dt_args)


def datetime_workaround(string_date, format="%Y-%m-%d", date_only=True):
    if string_date == '':
        return None
    try:
        if date_only:
            res = datetime.datetime.strptime(string_date, format).date()
        else:
            res = datetime.datetime.strptime(string_date, format)
    except TypeError:
        if date_only:
            res = datetime.datetime(*(time.strptime(string_date, format)[0:6])).date()
        else:
            res = datetime.datetime(*(time.strptime(string_date, format)[0:6]))

    return res


def shortened_debrid(debrid):
    debrid = debrid.lower()
    if debrid == 'premiumize':
        return 'PM'
    if debrid == 'real_debrid':
        return 'RD'
    return ''


def source_size_display(size):
    size = int(size)
    size = float(size) / 1024
    size = "{0:.2f} GB".format(size)
    return size


def color_quality(quality):
    color = 'darkred'

    if quality == '4K':
        color = 'lime'
    if quality == '1080p':
        color = 'greenyellow'
    if quality == '720p':
        color = 'sandybrown'
    if quality == 'SD':
        color = 'red'

    return colorString(quality, color)


def context_addon():
    if condVisibility('System.HasAddon(context.seren)'):
        return True
    else:
        return False


def get_language_code():
    from resources.lib.common import languageCodes

    for code in languageCodes.isoLangs:
        if languageCodes.isoLangs[code]['name'].lower() == language.lower():
            language_code = code
    # Continue using en until everything is tested to accept other languages
    language_code = 'en'
    return language_code


def paginate_list(list_items, page, limit):
    pages = [list_items[i:i + limit] for i in xrange(0, len(list_items), limit)]
    return pages[page - 1]


def setSetting(id, value):
    return xbmcaddon.Addon().setSetting(id, value)



def getSetting(id):
    return xbmcaddon.Addon().getSetting(id)


def premiumize_enabled():
    if getSetting('premiumize.pin') != '' and getSetting('premiumize.enabled') == 'true':
        return True
    else:
        return False

def real_debrid_enabled():
    if getSetting('rd.auth') != '' and getSetting('realdebrid.enabled') == 'true':
        return True
    else:
        return False