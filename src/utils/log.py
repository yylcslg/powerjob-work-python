import logging
import os
from logging import handlers

from src.task_core.instance_log_queue import logQueue
from src.web.bean.instance_log import InstanceLogContent


class Web3log:

    default_format = "%(asctime)s-process[%(process)d]-[%(levelname)s]:%(message)s"

    def __init__(self, log_name='powerjob-work-python', log_level = "INFO", max_mb = 10, format_str = default_format):
        log = logging.getLogger(log_name)
        log.setLevel(log_level)

        dir_path = os.path.abspath(os.path.dirname(__file__)) + '/../../log/'

        fh = handlers.RotatingFileHandler(dir_path + log_name + ".log", maxBytes=max_mb * 1024 * 1024, backupCount=100000)
        fh.setLevel(log_level)
        log.addHandler(fh)
        fh.setFormatter(logging.Formatter(format_str))

        self.log = log


    def msg_info(self, msg, id=0, print_flag:bool = True, *args, **kwargs):
        if print_flag:
            print('[info]', msg, *args)
        self.log.info(msg, *args, **kwargs)
        if id > 0:
            logQueue.queue.put(InstanceLogContent.buildLog(id, msg))
            pass

    def msg_error(self, msg, print_flag: bool = True, *args, **kwargs):
        if print_flag:
            print(msg,*args)
        self.log.error(msg,*args, **kwargs)



worker_log = Web3log(log_name='powerjob-work', log_level = "INFO")
log_error = Web3log(log_name='powerjob-work-error', log_level='ERROR')