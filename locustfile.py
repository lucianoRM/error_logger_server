import json
import random
import string

import time
from locust import HttpLocust, TaskSet, task
class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.maxPackageDepth = 3
        self.maxStackTraceDepth = 50
        self.appNames = []
        self.packages = ['com','org','lang','java','junit','apache','json']
        self.classesPrefixes = ['Array','Map','Config','Interval','String','Stack','Pointer','Parser','Chart','Counter','HTTPRequest','HTTPResponse','Handler','Graph']
        self.classesSufixes = ['IndexOutOfBounds','IsNull','TypeIsInvalid','TooShort','ConfigutationIsInvalid','Malformed','NameNotFound','Overflow']
        self.methods = ['doThis','doThat','dontDo','doOtherThing','stop','start','run','create','invoke','parse','drop','commit','rollback','push','pop']
        self.exception = 'Exception'
        self.apps = ['FIFA','AngryBirds','NBA','NHL','NeedForSpeed','ClashRoyale','CounterStrike','CallOfDuty','Battlefield','PES','Doom','Sims','Tycoon','Minecraft','Mario','Zelda','Pokemon']
        self.versions = ['75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17']


    def createException(self):
        exception = ''
        for i in range(random.choice(range(self.maxPackageDepth))):
            exception += random.choice(self.packages)
            exception += '.'
        exception += random.choice(self.classesPrefixes)
        exception += random.choice(self.classesSufixes)
        exception += self.exception
        return exception

    def createFunctionCall(self):
        functioncall = ''
        for i in range(random.choice(range(self.maxPackageDepth))):
            functioncall += random.choice(self.packages)
            functioncall += '.'
        functioncall += random.choice(self.classesPrefixes)
        functioncall += "."
        functioncall += random.choice(self.methods)
        functioncall += '()'
        return functioncall


    def createStackTrace(self, exception):
        stacktrace = exception
        for i in range(random.choice(range(self.maxStackTraceDepth))):
            stacktrace+="\n\tat "
            stacktrace+=self.createFunctionCall()
        return stacktrace



    @task(1)
    def sendError(self):
        exception = self.createException()
        dicc = {
            "userName" : "luciano",
            "appName" : random.choice(self.apps) + random.choice(self.versions),
            "timestamp" : int(time.time()),
            "os" : "Linux",
            "errorText" : exception,
            "stacktrace" : self.createStackTrace(exception)
        }
        self.client.post('/errors',json=json.dumps(dicc))

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 10000
    max_wait = 600000
