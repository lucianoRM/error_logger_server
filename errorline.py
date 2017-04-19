from google.appengine.ext import ndb

class ErrorLine(ndb.Model):
    lineString = ndb.StringProperty()
