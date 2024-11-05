import json
from enum import Enum

from src.utils import tools_utils
from src.utils.Properties import pro
from src.utils.constance_util import constance
from src.web.bean.job_req import JobReq

class InstanceBean:
    def __init__(self, data=None):
        workerAddress = tools_utils.local_host_ip() + ":" + pro.get("powerjob.worker.port")
        self.appId = constance.app_id
        self.jobId = 1
        self.instanceId=1
        self.instanceStatus=2
        self.needAlert = False
        self.reportTime =0
        self.sourceAddress =workerAddress
        self.startTime=0
        self.endTime=0
        self.succeedTaskNum=0
        self.totalTaskNum=0
        self.failedTaskNum=0
        self.alertContent=''
        self.result=''

        if data:
            self.__dict__ = data


    @staticmethod
    def buildInstanceBean(b:JobReq):
        bean = InstanceBean()
        bean.jobId = b.jobId
        bean.instanceId = b.instanceId
        bean.instanceStatus = Instance_status.WAIT_WORK_RECIVE.value
        bean.needAlert = False
        bean.reportTime = 0
        bean.succeedTaskNum = 0
        bean.totalTaskNum = 0
        bean.failedTaskNum = 0
        return bean

    def toJsonStr(self):
        return json.dumps(self.__dict__)


    #instanceStatus 1:"等待派发"
    # 2, "等待Worker接收"
    # 3, "运行中"
    # 4, "失败"
    # 5, "成功"
    # 9, "取消"
    # 10, "手动停止"
class Instance_status(Enum):
    WAIT_DISPATCH = (1)
    WAIT_WORK_RECIVE = (2)
    RUNING = (3)
    FAIL = (4)
    SUCCESS = (5)
    CANCEL = (9)
    STOP = (10)