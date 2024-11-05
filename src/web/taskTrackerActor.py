import json
from time import sleep

from flask import request

from src.cache.cache import instanceCache
from src.utils.date_utils import DateUtils
from src.utils.thread_pool import job_process_thread
from src.web import taskTracker
from src.web.bean.instance_bean import InstanceBean
from src.web.processorTrackerActor import task_process


@taskTracker.route('/a')
def hello():
    return 'Hello,taskTracker!'



def task_tracker(bean: InstanceBean):
    bean.startTime = DateUtils.get_timestamp()
    instanceCache[bean.instanceId] = bean
    job_process_thread.submit(task_process, bean)



