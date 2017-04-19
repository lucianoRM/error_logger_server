from google.appengine.ext import ndb


class Application(ndb.Model):
    appName = ndb.StringProperty()

    @classmethod
    def queryApp(cls, appName):
        return cls.query(cls.appName == appName)


    @classmethod
    def queryAll(cls):
        return cls.query()


def createIfNotExistent(appName):
    app = Application.queryApp(appName).fetch()
    if not app:
        app = Application(appName=appName)
        app.put()

def getApp(appName):
    return Application.queryApp(appName).fetch()

def getAllApps():
    return Application.queryAll().fetch()