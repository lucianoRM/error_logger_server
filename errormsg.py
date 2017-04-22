
from google.appengine.ext import ndb

import application
import counter


class ErrorMessage(ndb.Model):
    userName = ndb.StringProperty(indexed=False)
    appName = ndb.StringProperty()
    timestamp = ndb.IntegerProperty()
    os = ndb.StringProperty()
    errorText = ndb.StringProperty()


@ndb.transactional
def store(errorMessage):
    errorMessage.put()
