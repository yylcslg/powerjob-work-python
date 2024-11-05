import json
from time import sleep

import requests

from src.cache.cache import instanceCache, taskCache
from src.task_core.instance_log_queue import logQueue
from src.utils import tools_utils
from src.utils.Properties import pro
from src.utils.date_utils import DateUtils
from src.utils.constance_util import constance
from src.web.bean.instance_bean import InstanceBean, Instance_status
from src.web.bean.work_log import WorkLog

HTTP_PREFIX='http://'

class WorkReporter:

    def __init__(self):
        server_ip = pro.get("powerjob.worker.server-address")
        self.app_name = pro.get("powerjob.worker.app-name")
        realUrl = HTTP_PREFIX + server_ip + '/server/assert?appName=' + self.app_name
        self.app_id = requests.get(realUrl).json()['data']
        constance.app_id=self.app_id
        app_info_url = HTTP_PREFIX + server_ip + '/server/acquire?protocol=HTTP&appId=' + str(self.app_id)
        self.server_address = requests.get(app_info_url).json()['data']


    def reportHealth(self):
        while True:
            try:
                url = HTTP_PREFIX +self.server_address+'/server/workerHeartbeat'
                workerAddress = tools_utils.local_host_ip() + ":" + pro.get("powerjob.worker.port")
                ts = DateUtils.get_timestamp()
                json = {"appId": self.app_id,
                        "appName": self.app_name,
                        "client":"KingPenguin",
                        "containerInfos":[],
                         "heartbeatTime":ts,
                        "heavyTaskTrackerNum":0,
                        "lightTaskTrackerNum":0,
                        "overload":'false',
                         "protocol":"HTTP",
                        "systemMetrics":{"cpuLoad":2,"cpuProcessors":20,"diskTotal":875,"diskUsage":0.124,"diskUsed":108.5645,"jvmMaxMemory":16,"jvmMemoryUsage":0.0056,"jvmUsedMemory":0.0432,"score":87},
                         "version":"UNKNOWN",
                        "workerAddress":workerAddress}

                requests.post(url, json=json)
                sleep(5)
            except Exception as e:
                print('reportHealth error...', e)
                sleep(5)

    def reportInstanceStatus(self):
        url = HTTP_PREFIX + self.server_address + '/server/reportInstanceStatus'
        while True:
            try:
                for key in list(instanceCache.keys()):
                    if key in instanceCache:
                        bean:InstanceBean = instanceCache[key]
                        bean.reportTime = DateUtils.get_timestamp()
                        requests.post(url, json=json.loads(bean.toJsonStr()))

                        if (bean.instanceStatus == Instance_status.SUCCESS.value or
                            bean.instanceStatus == Instance_status.FAIL.value or
                            bean.instanceStatus == Instance_status.STOP.value or
                            bean.instanceStatus == Instance_status.CANCEL.value):
                            del instanceCache[key]
                            del taskCache[key]

                sleep(5)
            except Exception as e:
                print('reportHealth error...', e)
                sleep(5)



    def report_log(self):
        url = HTTP_PREFIX + self.server_address + '/server/reportLog'
        workerAddress = tools_utils.local_host_ip() + ":" + pro.get("powerjob.worker.port")
        log = WorkLog()
        log.workerAddress = workerAddress
        ts = DateUtils.get_timestamp()
        num = 0
        while True:
            try:
                gap = DateUtils.get_timestamp() - ts
                if logQueue.queue.empty():
                    if (gap > 10000 and len(log.instanceLogContents) >0):
                        requests.post(url, json=json.loads(log.toJSON()))
                        log.instanceLogContents=[]
                        ts = DateUtils.get_timestamp()
                        num = 0
                    sleep(1)
                else:
                    j = logQueue.queue.get()
                    log.instanceLogContents.append(j)

                    num = num + 1
                    if (gap > 10000 or num > 100):
                        requests.post(url, json=json.loads(log.toJSON()))
                        log.instanceLogContents=[]
                        ts = DateUtils.get_timestamp()
                        num = 0
            except Exception as e:
                print('report_log error...', e)
                sleep(1)




workReport = WorkReporter()