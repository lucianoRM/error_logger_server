import datetime
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
    timestamp = datetime.datetime.fromtimestamp(jsonObject['timestamp'])
    os = str(jsonObject['os'])
    errorText = str(jsonObject['errorText'])
    return errormsg.ErrorMessage(userName=userName, appName=appName,
                                 timestamp=timestamp, os=os,
                                 errorText=errorText)

def storeFromJson(jsonString):
    errorMessage = createErrorMsgFromJson(jsonString)
    errormsg.store(errorMessage)
    application.upsert(errorMessage.appName)


def toDicc(appList):
    dicc = {}
    for app in appList:
        dicc[app.appName] = counter.get_count(app.appName)
    return dicc


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


def getAppCount(pagenumber):
    return application.getAllApps(pagenumber)