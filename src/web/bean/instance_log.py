import json

from src.utils.date_utils import DateUtils


class InstanceLogContent:
    def __init__(self, data=None):
        self.instanceId=0
        self.logTime=0
        self.logLevel=1
        self.logContent=''

        if data:
            self.__dict__ = data

    def toJsonStr(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def buildLog(instanceId,logContent):
        bean = InstanceLogContent()
        bean.instanceId = instanceId
        bean.logTime = DateUtils.get_timestamp()
        bean.logContent = logContent
        return bean




