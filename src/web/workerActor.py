import json

from flask import request

from src.cache.cache import instanceCache, taskCache
from src.utils.log import log
from src.web import worker
from src.web.bean.instance_bean import InstanceBean
from src.web.bean.job_req import JobReq
from src.web.taskTrackerActor import task_tracker


@worker.route('/runJob',methods=['POST'])
def runJob():
    jsonDataStr = request.stream.read().decode()
    jobReq = json.loads(jsonDataStr, object_hook=JobReq)
    instanceBean = InstanceBean.buildInstanceBean(jobReq)

    if jobReq.instanceId in taskCache:
        return 'run job'


    #cache
    taskCache[jobReq.instanceId] = jobReq
    instanceCache[jobReq.instanceId] = instanceBean

    task_tracker(instanceBean)
    return 'runJob!'



@worker.route('/stopInstance',methods=['POST'])
def stopInstance():
    data = json.loads(request.stream.read().decode())
    instanceId = data['instanceId']
    log.info(f'worker stopInstance:, {instanceId}')
    if instanceId in instanceCache:
        bean : InstanceBean = instanceCache[instanceId]
        bean.result = 'stop'

    return 'Hello, World!'

@worker.route('/queryInstanceStatus',methods=['POST'])
def queryInstanceStatus():
    print('worker queryInstanceStatus')
    data = json.loads(request.stream.read().decode())

    print('queryInstanceStatus:.', data)
    return 'Hello, World!'
