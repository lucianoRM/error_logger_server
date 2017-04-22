import datetime
import time
import json

import application
import counter
import errormsg


def createErrorMsgFromJson(jsonString):
    jsonObject = json.loads(jsonString)
    while(type(jsonObject) == unicode):
        jsonObject = json.loads(jsonObject)
    userName = str(jsonObject['userName'])
    appName = str(jsonObject['appName'])
    timestamp = int(jsonObject['timestamp'])
    os = str(jsonObject['os'])
    errorText = str(jsonObject['errorText'])
    return errormsg.ErrorMessage(userName=userName, appName=appName,
                                 timestamp=timestamp, os=os,
                                 errorText=errorText)

def storeFromJson(jsonString):
    errorMessage = createErrorMsgFromJson(jsonString)
    errormsg.store(errorMessage)
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


def getAppCount(date,pagenumber):
    try:
        timestamp = int(time.mktime(datetime.datetime.strptime(date, '%Y%m%d%H%M%S').timetuple()))
    except:
        timestamp = int(time.time())
    return application.getAllApps(timestamp, pagenumber)