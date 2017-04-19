import datetime
import json

import application
import counter
import errormsg


def createErrorMsgFromJson(jsonString):
    jsonObject = json.loads(jsonString)
    userName = jsonObject['userName']
    appName = jsonObject['appName']
    timestamp = datetime.datetime.fromtimestamp(jsonObject['timestamp'])
    os = jsonObject['os']
    errorText = jsonObject['errorText']
    return errormsg.ErrorMessage(userName=userName, appName=appName,
                                 timestamp=timestamp, os=os,
                                 errorText=errorText)

def storeFromJson(jsonString):
    errorMessage = createErrorMsgFromJson(jsonString)
    errormsg.store(errorMessage)
    application.createIfNotExistent(errorMessage.appName)
    counter.increment(errorMessage.appName)


def toDicc(appList):
    dicc = {}
    for app in appList:
        dicc[app.appName] = counter.get_count(app.appName)
    return dicc

def getAppCount(app=None):
    if not app:
        return toDicc(application.getAllApps())
    else:
        return toDicc(application.getApp([app]))