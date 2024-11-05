import json


class JobReq:
    def __init__(self, data=None):
        self.allWorkerAddress = []
        self.maxWorkerCount = 0
        self.jobId = 0
        self.instanceId = 0
        self.executeType ='STANDALONE'
        self.processorType='BUILT_IN'
        self.jobParams=''
        self.processorInfo=''
        self.instanceParams = ''
        self.instanceTimeoutMS = 0
        self.threadConcurrency = 1
        self.taskRetryNum=1
        self.timeExpressionType='FIXED_RATE'
        self.timeExpression = '3000'
        self.maxInstanceNum = 1
        self.alarmConfig=''
        self.logConfig=''
        self.advancedRuntimeConfig=''

        if data:
            self.__dict__ = data


    def toJsonStr(self):
        return json.dumps(self.__dict__)
