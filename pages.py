from google.appengine.api import memcache
from google.appengine.ext import ndb

from config import config

class LastPage(ndb.Model):
    last = ndb.IntegerProperty(default=0)


class Pages(ndb.Model):
    contents = ndb.StringProperty(repeated=True)


def createPageKey(name,timestamp,number):
    return config.page_key_template().format(name, str(timestamp), number)

def createTotalKey(name,timestamp):
    return config.page_total_key_template().format(name, str(timestamp))

def updateLastPage(newIndex,id):
    lastPage = LastPage(last=newIndex,id=id)
    updateFuture = lastPage.put_async()
    memcache.set(key=id,value=newIndex)
    updateFuture.check_success()

def upsert(keyName,timestamp,value):
    lastPage = LastPage.get_by_id(createTotalKey(keyName, timestamp))
    if not lastPage:
        lastPage = LastPage(last=0, id=createTotalKey(keyName,timestamp))
        lastPage.put_async()
    lastIndex = lastPage.last
    page = Pages.get_by_id(createPageKey(keyName, timestamp, lastIndex))
    if not page:
        contents = []
    else:
        contents = page.contents
        if len(contents) == config.page_max_count():
            lastIndex = lastIndex + 1
            updateLastPage(newIndex=lastIndex,id=createTotalKey(keyName,timestamp))
            contents = []
    contents.append(value)
    page = Pages(contents=contents, id=createPageKey(keyName, timestamp, lastIndex))
    updateFuture = page.put_async()
    memcache.set(key=createPageKey(keyName, timestamp, lastIndex), value=contents)
    updateFuture.check_success()

def getPage(keyName,timestamp,pagenumber):
    lastIndex = getLastIndex(keyName,timestamp)
    if(pagenumber > lastIndex):
        pagenumber = lastIndex
    contents = memcache.get(createPageKey(keyName,timestamp,pagenumber))
    if not contents:
        pages = Pages.get_by_id(createPageKey(keyName,timestamp,pagenumber))
        if not pages:
            contents = []
        else:
            contents = pages.contents
            memcache.set(key=createPageKey(keyName,timestamp,pagenumber),value=contents)
    return contents, pagenumber

def getLastIndex(keyName,timestamp):
    totalKey = createTotalKey(keyName,timestamp)
    lastIndex = memcache.get(totalKey)
    if not lastIndex:
        lastPage = LastPage.get_by_id(totalKey)
        if not lastPage:
            lastPage = LastPage(id=totalKey,last=0)
            lastPage.put()
        memcache.set(key=lastPage.key.id(), value=lastPage.last)
        lastIndex = lastPage.last
    return lastIndex
