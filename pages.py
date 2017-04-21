from google.appengine.api import memcache
from google.appengine.ext import ndb

from config import config

class LastPage(ndb.Model):
    last = ndb.IntegerProperty(default=0)


class Pages(ndb.Model):
    contents = ndb.StringProperty(repeated=True)


def createKey(name,number):
    return config.page_key_template().format(name, number)

def updateLastPage(newIndex,id):
    lastPage = LastPage(last=newIndex,id=id)
    lastPage.put()

def upsert(keyName,value):
    lastPage = LastPage.get_by_id(config.page_total_key_template().format(keyName))
    if not lastPage:
        lastPage = LastPage(last=0, id=config.page_total_key_template().format(keyName))
        lastPage.put_async()
    lastIndex = lastPage.last
    page = Pages.get_by_id(createKey(keyName, lastIndex))
    if not page:
        contents = []
    else:
        contents = page.contents
        if len(contents) == config.page_max_count():
            lastIndex = lastIndex + 1
            updateLastPage(newIndex=lastIndex,id=config.page_total_key_template().format(keyName))
            contents = []
    contents.append(value)
    page = Pages(contents=contents, id=createKey(keyName,lastIndex))
    page.put()

def getPage(keyName,pagenumber):
    lastIndex = getLastIndex(keyName)
    if(pagenumber > lastIndex):
        pagenumber = lastIndex
    contents = memcache.get(config.page_key_template().format(keyName,pagenumber))
    if not contents:
        pages = Pages.get_by_id(config.page_key_template().format(keyName,pagenumber))
        if not pages:
            contents = []
        else:
            contents = pages.contents
            memcache.set(key=config.page_key_template().format(keyName,pagenumber),value=contents)
    return contents,pagenumber

def getLastIndex(keyName):
    lastIndex = memcache.get(config.page_total_key_template().format(keyName))
    if not lastIndex:
        lastPage = LastPage.get_by_id(config.page_total_key_template().format(keyName))
        if not lastPage:
            lastPage = LastPage(id=config.page_total_key_template().format(keyName),last=0)
            lastPage.put()
        memcache.set(key=lastPage.key.id(), value=lastPage.last)
        lastIndex = lastPage.last
    return lastIndex
