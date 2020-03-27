# -*- coding: utf-8 -*-

import xbmc

from resources.lib.modules import tools
from resources.lib.modules import accounts

tools.log('HUMMINGBIRD - STARTING SERVICE')
monitor = xbmc.Monitor()

tools.log('Making sure your still logged in cause the addon breaks if your not...')

login_status = tools.checkLoginStatus()
if login_status == True:
    accounts.Kitsu().login(silent=True)
    accounts.Mal().login(silent=True)
    accounts.Anilist().login(silent=True)
    
tools.log('Successfully logged in again to make the addon work...')

while not monitor.abortRequested():
    try:
        if monitor.waitForAbort(60 * 15):
            break
    except:
        continue