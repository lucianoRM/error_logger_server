from google.appengine.ext import ndb

import counter
from config import config


class ErrorLine(ndb.Model):
    lineString = ndb.StringProperty()
    total = ndb.IntegerProperty(default=0)
    timeInterval = ndb.IntegerProperty()
    updated = ndb.BooleanProperty(default=True)

    @classmethod
    def getLinesToUpdate(cls,timeInterval):
        return cls.query(ErrorLine.timeInterval == timeInterval, ErrorLine.updated == True)

    @classmethod
    def getLinesToDisplay(cls,timeInterval):
        return cls.query(ErrorLine.timeInterval == timeInterval).order(ErrorLine.total)


def createKey(lineString, timestamp):
    return config.error_line_key_template().format(lineString, timestamp)


def getTimeInterval(timestamp):
    remainder = timestamp % config.top_reset_time()
    return timestamp - remainder

def upsertMulti(errorList, timestamp):
    timeInterval = getTimeInterval(timestamp)
    keys = []
    for error in errorList:
        keys.append(ndb.Key(ErrorLine, createKey(error,timeInterval)))
    futuresList = ndb.get_multi_async(keys)
    for key in keys:
        updateCounter(key.id())
    toUpdate = []
    index = 0
    for future in futuresList:
        error = future.get_result()
        if not error:
            toUpdate.append(ErrorLine(lineString=errorList[index],
                                      timeInterval=timeInterval,
                                      id=(keys[index]).id()))
        elif error.updated is False:
            error.updated = True
            toUpdate.append(error)

        index+=1

    ndb.put_multi(toUpdate)

def updateCounter(key):
    counter.increment(key)


def updateTotal(timestamp):
    timeInterval = getTimeInterval(timestamp)
    lines = ErrorLine.getLinesToUpdate(timeInterval).fetch()
    print lines
    counterValuesFutures = []
    for line in lines:
        counterValuesFutures.append(counter.get_count_async(line.key.id()))
    index = 0
    for line in lines:
        line.total = counter.getTotal((counterValuesFutures[index]))
        line.updated = False
        index += 1
    ndb.put_multi(lines)

def getTop(timestamp):
    timeInterval = getTimeInterval(timestamp)
    n = config.top_quantity()
    topN = ErrorLine.getLinesToDisplay(timeInterval).fetch(n)
    dicc = {}
    for line in topN:
        dicc[line.lineString] = line.total
    return dicc, timeInterval