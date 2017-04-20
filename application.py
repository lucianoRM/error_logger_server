from google.appengine.api import memcache
from google.appengine.ext import ndb

import counter


class Application(ndb.Model):
    appName = ndb.StringProperty()

    @classmethod
    def queryAll(cls):
        return cls.query()


def upsert(appName):
    app = Application.get_by_id_async(appName)
    memcache.incr(key=appName)
    counter.increment(appName)
    if not app.get_result():
        app = Application(appName=appName)
        app.put()


def getAppCount(appName):
    app = memcache.get(appName)
    if not app:
        return Application.get_by_id(appName)

def getAppNames():
    return Application.queryAll().fetch()

def getAllApps():
    apps = getAppNames()
    appCount = memcache.get_multi([app.appName for app in apps])
    missing_keys_futures = {}

    for app in apps: #Check if all apps are in dictionary
        if not appCount.has_key(app.appName):
            missing_keys_futures[app.appName] = counter.get_count_async(app.appName)

    memcache_update = {}
    #Add results to dictionary
    for key in missing_keys_futures.keys():
        total = counter.getTotal(missing_keys_futures[key])
        appCount[key] = total #should call getTotal because counter.get_count_async returns a list of futures for every shard
        memcache_update[key] = total

    # add missing keys to memcache
    memcache.set_multi(memcache_update)
    return appCount

