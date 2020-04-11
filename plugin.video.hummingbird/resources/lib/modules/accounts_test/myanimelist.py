import requests
import json
import re

from . import account_info
from resources.lib.modules import tools

class List:
    def __init__(self):
        self.site = 'https://myanimelist.net'
        self.username = tools.getSetting('mal.user')

    def getCurrent(self):
        data_items = []
        mal_anime = []
        kitsu_ids = []
        
        sort_status = tools.getSetting('current.sort') 
        sort = account_info.account_sort['mal'][sort_status] % '1'

        resp = requests.get(self.site + '/animelist/%s?%s' % (self.username, sort))
        items = re.findall(r'<table class="list-table" data-items="(.*?)">', str(resp.content))[0]
        data_items = items.replace('&quot;', '"')
        data_items = json.loads(data_items)
        for a in data_items:
            mal_anime.append({'id': a['anime_id'], 'status': 'current', 'progress': a['num_watched_episodes']})
        
        mal_data = MyAnimeList().get_data(mal_anime)
        
        if '-' in sort_status:
            mal_data = sorted(mal_data, reverse=True)
        
        return mal_data
        
    def getFinished(self):
        data_items = []
        mal_anime = []
        kitsu_ids = []
        
        sort_status = tools.getSetting('finished.sort') 
        sort = account_info.account_sort['mal'][sort_status] % '2'

        resp = requests.get(self.site + '/animelist/%s?%s' % (self.username, sort))
        items = re.findall(r'<table class="list-table" data-items="(.*?)">', str(resp.content))[0]
        data_items = items.replace('&quot;', '"')
        data_items = json.loads(data_items)
        for a in data_items:
            mal_anime.append({'id': a['anime_id'], 'status': 'finished', 'progress': a['num_watched_episodes']})
        
        mal_data = MyAnimeList().get_data(mal_anime)
        
        
        if '-' in sort_status:
            mal_data = sorted(mal_data, reverse=True)
        
        return mal_data
        
    def getDropped(self):
        data_items = []
        mal_anime = []
        kitsu_ids = []
        
        sort_status = tools.getSetting('dropped.sort') 
        sort = account_info.account_sort['mal'][sort_status] % '4'

        resp = requests.get(self.site + '/animelist/%s?%s' % (self.username, sort))
        items = re.findall(r'<table class="list-table" data-items="(.*?)">', str(resp.content))[0]
        data_items = items.replace('&quot;', '"')
        data_items = json.loads(data_items)
        for a in data_items:
            mal_anime.append({'id': a['anime_id'], 'status': 'dropped', 'progress': a['num_watched_episodes']})
        
        mal_data = MyAnimeList().get_data(mal_anime)

        if '-' in sort_status:
            mal_data = sorted(mal_data, reverse=True)
        
        return mal_data
        
    def getHold(self):
        data_items = []
        mal_anime = []
        kitsu_ids = []
        
        sort_status = tools.getSetting('hold.sort') 
        sort = account_info.account_sort['mal'][sort_status] % '3'

        resp = requests.get(self.site + '/animelist/%s?%s' % (self.username, sort))
        items = re.findall(r'<table class="list-table" data-items="(.*?)">', str(resp.content))[0]
        data_items = items.replace('&quot;', '"')
        data_items = json.loads(data_items)
        for a in data_items:
            mal_anime.append({'id': a['anime_id'], 'status': 'onhold', 'progress': a['num_watched_episodes']})
        
        mal_data = MyAnimeList().get_data(mal_anime)
        
        if '-' in sort_status:
            mal_data = sorted(mal_data, reverse=True)
        
        return mal_data

    def getPlanned(self):
        data_items = []
        mal_anime = []
        kitsu_ids = []
        
        sort_status = tools.getSetting('planned.sort') 
        sort = account_info.account_sort['mal'][sort_status] % '6'

        resp = requests.get(self.site + '/animelist/%s?%s' % (self.username, sort))
        items = re.findall(r'<table class="list-table" data-items="(.*?)">', str(resp.content))[0]
        data_items = items.replace('&quot;', '"')
        data_items = json.loads(data_items)
        for a in data_items:
            mal_anime.append({'id': a['anime_id'], 'status': 'planned', 'progress': a['num_watched_episodes']})
        
        mal_data = MyAnimeList().get_data(mal_anime)
        
        if '-' in sort_status:
            mal_data = sorted(mal_data, reverse=True)
            
        return mal_data
            
class MyAnimeList:
    def __init__(self):
        self.site = 'https://myanimelist.net'
        
        self.username = tools.getSetting('mal.user')
        self.password = tools.getSetting('mal.pass')
        
        self.logsessid = tools.getSetting('mal.logsess')
        self.sessionid = tools.getSetting('mal.sessionid')
        
        self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept': '*/*',
                'Cookie': 'MALHLOGSESSID=%s; MALSESSIONID=%s; is_logged_in=1; anime_update_advanced=1' % (self.logsessid, self.sessionid),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 \Firefox/56.0',
                }

    def login(self):
        session = requests.session()
        crsf_res = session.get(self.site).text
        crsf = (re.compile("<meta name='csrf_token' content='(.+?)'>").findall(crsf_res))[0]
        payload = {
            "user_name": self.username,
            "password": self.password,
            "cookie": 1,
            "sublogin": "Login",
            "submit": 1,
            "csrf_token": crsf
            }        
        url = self.site + '/login.php?from=%2F'
        session.get(url)
        result = session.post(url, data=payload)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', attrs={'class': 'badresult'})
        if results:
            if silent != True:
                tools.showDialog.notification(tools.addonName, 'MAL - Login Unsuccessful')
            else:
                tools.log('MAL - Login Unsuccessful')
            return
        
        tools.setSetting('mal.logsess', str(session.cookies['MALHLOGSESSID']))
        tools.setSetting('mal.sessionid', str(session.cookies['MALSESSIONID']))
        
        if silent != True:
            tools.showDialog.notification(tools.addonName, 'MAL - Logged in successfully')
        else:
            tools.log('MAL - Logged in successfully')
        
        return

    def get_data(self, list):
        anime_pages = []
        got_data = []
        for a in list:
            resp = requests.get('https://myanimelist.net/anime/%s' % a['id'])
            got_data.append(self.get_info(resp.content, a['id'], a['status'], a['progress']))
            
        return got_data
            
    def get_info(self, html, id, watch_status, progress):
        load = str(html)
        #Regex out all required data
        #Titles
        try: 
            base = re.findall(r'<span class="h1-title"><span itemprop="name">(.*?)</span>', load)[0]
            try:
                base = base.split('<br>')[0]
            except:
                pass
        except: 
            base = None
        try: english = re.findall(r'English:</span> (.*?)\\n', load)[0]
        except: english = None
        try: japanese = re.findall(r'Japanese:</span> (.*?)\\n', load)[0]
        except: japanese = None
        #Data
        try: type = re.findall(r'Type:</span>\\n  <a href=".*?">(.*?)</a>', load)[0]
        except: type = None
        try: episodes = re.findall(r'Episodes:</span>\\n  (.*?)\\n', load)[0]
        except: episodes = None
        try: status = re.findall(r'Status:</span>\\n  (.*?)\\n', load)[0]
        except: status = None
        try: year = re.findall(r'Premiered:</span>\\n          <a href=".*?">.*? (.*?)</a>', load)[0]
        except: year = None
        try: genres = ', '.join(re.findall(r'<span itemprop="genre" style="display: none">(.*?)</span>', load))
        except: genres = None
        try: picture = re.findall(r'<img class="lazyload" data-src="(.*?)" alt=".*?" class="ac" itemprop="image">', load)[0]
        except: picture = None
        try: 
            plot = re.findall(r'<span itemprop="description">(.*?)</span>', load)[0]
            plot = self.strip_text(plot)
        except:
            plot = None
        
        dict = {
            'id': id,
            'titles': {
                 'base': base, 
                 'english': english, 
                 'japanese': japanese
                 },
            'subtype': type,
            'episode_count': episodes,
            'status': status,
            'plot': plot,
            'year': year,
            'genres': genres,
            'picture': picture,
            'account_info': {
                'status': watch_status,
                'progress': progress
                }
            }          
        
        return dict
        
    def strip_text(self, text):
        #Remove all stupid html bits and replace nonsense
        new_text = text.replace('<br />', ' ')
        new_text = new_text.replace('\\r\\n', '')
        new_text = new_text.replace('<i>', '')
        new_text = new_text.replace('</i>', '')
        new_text = new_text.replace('&quot;', '"')
        new_text = new_text.replace('&#039;', "'")
        return new_text
