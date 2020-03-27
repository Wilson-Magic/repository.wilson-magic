# -*- coding: utf-8 -*-

import ast
import hashlib
import re
import time

from resources.lib.modules import tools

try:
    from sqlite3 import dbapi2 as db, OperationalError
except:
    from pysqlite2 import dbapi2 as db, OperationalError
    
#Was originally using the same caching from Masterani Redux, it was... insufficient to say the least, so I wrote my own based on Seren's :P

class hummingCache:
    def cacheCheck(self, function, duration, *args, **kwargs):
        try:
            key = cacheLib().hashFunction(function, args, kwargs)
            cache_result = cacheLib().get(key)
            if cache_result:
                if cacheLib().validityCheck(cache_result['date'], duration):
                    try:
                        return_data = ast.literal_eval(cache_result['value'])
                        return return_data
                    except:
                        return ast.literal_eval(cache_result['value'])
            fresh_result = repr(function(*args, **kwargs))
            if not fresh_result or fresh_result is None or fresh_result == None:
                if cache_result:
                    return cache_result
                return None
            
            data = ast.literal_eval(fresh_result)
            cacheLib().insert(key, fresh_result)
            
            return data
        except Exception:
            import traceback
            traceback.print_exc()
            return None
            
    def accessCheck(self, token):
        cache_result = cacheLib().accessCheck(token)
        if cache_result:
            if cacheLib().accessValidity(cache_result['time'], cache_result['expiry']):
                return True
            else:
                return False
        else:
            return False
        
class providerDB:
    def __init__(self):
        self.twat = []        
        
class cacheLib:
    def __init__(self):
        self.cache_table = 'cache'
        self.kitsu_table = 'kitsu'

    def hashFunction(self, function_instance, *args):
        return self.functionName(function_instance) + self.generateHash(args)
        
    def functionName(self, function_instance):
        return re.sub('.+\smethod\s|.+function\s|\sat\s.+|\sof\s.+', '', repr(function_instance))        
            
    def generateHash(self, *args):
        md5_hash = hashlib.md5()
        try:
            [md5_hash.update(str(arg)) for arg in args]
        except:
            [md5_hash.update(str(arg).encode('utf-8')) for arg in args]
        return str(md5_hash.hexdigest())        
        
    def get(self, key):
        try:
            cursor = dbLib().getConnCursor(tools.cacheFile)
            cursor.execute("SELECT * FROM %s WHERE key = ?" % self.cache_table, [key])
            results = cursor.fetchone()          
            cursor.close()
            return results
        except OperationalError:
            return None
            
    def accessCheck(self, token):
        try:
            cursor.dbLib().getConnCursor(tools.cacheFile)
            cursor.execute("SELECT * FROM %s WHERE access_token = ?" %self.kitsu_table, [token])
            results = cursor.fetchone()
            cursor.close()
            return results
        except OperationalError:
            return None
            
    def accessValidity(self, time, expiry):
        now = int(time.time())
        diff = now - expiry
        if diff <= time:
            return 'Expired'
        else:
            return None
            
    def accessInsert(self, access, refresh, expiry):
        try:
            cursor = dbLib().getConnCursor(tools.cacheFile)
            now = int(time.time())
            cursor.execute("CREATE TABLE IF NOT EXISTS %s (access_token TEXT, refresh_token TEXT, time INTEGER, expiry INTEGER, UNIQUE(access_token))" % self.kitsu_table)
            update_result = cursor.execute("UPDATE %s SET refresh_token=?,time=?,expiry=? WHERE access_token=?" % self.kitsu_table, (access, refresh, now, expiry))
            if update_result.rowcount is 0:
                cursor.execute("INSERT INTO %s Values (?, ?, ?, ?)" % self.kitsu_table, (access, refresh, now, expiry))
            cursor.connection.commit()
            cursor.close()
        except:
            try:
                cursor.close()
            except:
                pass
            import traceback
            traceback.print_exc()
            pass
    
    def validityCheck(self, cached_time, cache_timeout):
        now = int(time.time())
        diff = now - cached_time
        return (cache_timeout * 3600) > diff
        
    def insert(self, key, value):
        try:
            cursor = dbLib().getConnCursor(tools.cacheFile)
            now = int(time.time())
            cursor.execute("CREATE TABLE IF NOT EXISTS %s (key TEXT, value TEXT, date INTEGER, UNIQUE(key))" % self.cache_table)
            update_result = cursor.execute("UPDATE %s SET value=?,date=? WHERE key=?" % self.cache_table, (value, now, key))
            if update_result.rowcount is 0:
                cursor.execute("INSERT INTO %s Values (?, ?, ?)" % self.cache_table, (key, value, now))
                
            cursor.connection.commit()
            cursor.close()
        except: 
            try:
                cursor.close()
            except:
                pass
            import traceback
            traceback.print_exc()
            pass
            
    def clear(self):
        try:
            cursor = dbLib().getConnCursor(tools.cacheFile)
            for t in [self.cache_table, 'rel_list', 'rel_lib']:
                try:
                    cursor.execute("DROP TABLE IF EXISTS %s" % t)
                    cursor.execute("VACUUM")
                    cursor.connection.commit()
                except:
                    pass
            tools.showDialog.notification(tools.addonName + ': Cache', 'Cache Cleared', time=5000)
        except:
            pass

class dbLib:
    def getConnCursor(self, filepath):
        conn = self.getConnection(filepath)
        return conn.cursor()

    def getConnection(self, filepath):
        tools.makeFile(tools.dataPath)
        conn = db.connect(filepath)
        conn.row_factory = self.dictFactory  
        return conn

    def dictFactory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d            