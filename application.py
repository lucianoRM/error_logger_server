import datetime
from time import gmtime, time

from google.appengine.api import memcache
from google.appengine.ext import ndb

import counter
import pages
from config import config

APP_KEY = 'application'


class Application(ndb.Model):
    appName = ndb.StringProperty()

    @classmethod
    def queryAll(cls):
        return cls.query()

def createAppKey(appName,timestamp):
    return appName+"-"+str(timestamp)

def getTimeInterval(timestamp):
    remainder = timestamp % config.chart_reset_time()
    return timestamp - remainder

def upsert(appName,timestamp):
    timeInterval = getTimeInterval(timestamp)
    timeInterval = str(timeInterval)
    app = Application.get_by_id_async(createAppKey(appName,timeInterval))
    counter.increment(createAppKey(appName,timeInterval))
    if not app.get_result():
        app = Application(appName=appName, id=createAppKey(appName,timeInterval))
        app.put()
        pages.upsert(APP_KEY,timeInterval, createAppKey(appName, timeInterval))


def getAllApps(timestamp,pagenumber):
    timeInterval = getTimeInterval(timestamp)
    apps,pagenumber = pages.getPage(APP_KEY,getTimeInterval(timeInterval),pagenumber)
    appCount = memcache.get_multi(apps)
    missing_keys_futures = {}

    for app in apps: #Check if all apps are in dictionary
        if not appCount.has_key(app):
            missing_keys_futures[app] = counter.get_count_async(app)

    memcache_update = {}
    #Add results to dictionary
    for key in missing_keys_futures.keys():
        total = counter.getTotal(missing_keys_futures[key])
        appCount[key] = total #should call getTotal because counter.get_count_async returns a list of futures for every shard
        memcache_update[key] = total

    # add missing keys to memcache
    memcache.set_multi(memcache_update)
    return appCount, pagenumber, timeInterval

