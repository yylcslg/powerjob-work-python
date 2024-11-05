import json


class WorkLog:
    def __init__(self, data=None):
        self.workerAddress=''
        self.instanceLogContents =[]

        if data:
            self.__dict__ = data

    def toJsonStr(self):
        return json.dumps(self.__dict__)

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)