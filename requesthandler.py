import datetime
import time
import json

from google.appengine.api.taskqueue import taskqueue

import application
import counter
import errorline
import errormsg
import stacktraceparser


def createErrorMsgFromJson(jsonString):
    jsonObject = json.loads(jsonString)
    while(type(jsonObject) == unicode):
        jsonObject = json.loads(jsonObject)
    userName = str(jsonObject['userName'])
    appName = str(jsonObject['appName'])
    timestamp = int(jsonObject['timestamp'])
    os = str(jsonObject['os'])
    errorText = str(jsonObject['errorText'])
    stacktrace = str(jsonObject['stacktrace'])
    return errormsg.ErrorMessage(userName=userName, appName=appName,
                                 timestamp=timestamp, os=os,
                                 errorText=errorText,stacktrace=stacktrace)

def storeFromJson(jsonString):
    errorMessage = createErrorMsgFromJson(jsonString)
    #errormsg.store(errorMessage)
    errorline.upsertMulti(stacktraceparser.parseStackTrace(errorMessage.stacktrace),errorMessage.timestamp)
    application.upsert(errorMessage.appName, errorMessage.timestamp)


def getAppsCounterValuesAsync(appList):
    futureList = []
    for app in appList:
        futureList.append(counter.get_count_async(app.appName))
    return futureList


def toDiccFromFutures(apps,counters):
    dicc = {}
    for i in range(len(apps)):
        dicc[apps[i].appName] = counter.getTotal(counters[i])
    return dicc

def getTimestamp(date):
    try:
        timestamp = int(time.mktime(datetime.datetime.strptime(date, '%Y%m%d%H%M%S').timetuple()))
    except:
        timestamp = int(time.time())
    return timestamp

def getAppCount(date,pagenumber):
    timestamp = getTimestamp(date)
    return application.getAllApps(timestamp, pagenumber)

def getTop(date):
    timestamp = getTimestamp(date)
    return errorline.getTop(timestamp)


def handlecron(cursor):
    timestamp = int(time.time())
    return errorline.updateBatch(timestamp,cursor)
