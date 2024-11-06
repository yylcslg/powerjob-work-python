
from src.background.work_reporter import workReport
from src.utils import tools_utils
from src.utils.Properties import pro
from src.utils.log import worker_log
from src.utils.thread_pool import worker_report_thread
from flask import Flask

from src.web import worker, taskTracker, processorTracker


def init_blue_print():
    worker_log.msg_info("sssss222sss")
    app = Flask(__name__)
    # 将创建的蓝图注册到app
    app.register_blueprint(worker)
    app.register_blueprint(taskTracker)
    app.register_blueprint(processorTracker)

    host = tools_utils.local_host_ip()
    port = pro.get('powerjob.worker.port')
    #host = '0.0.0.0'
    app.run(host=host, port=port)



def init_work_health():
    worker_report_thread.submit(workReport.reportHealth)
    worker_report_thread.submit(workReport.reportInstanceStatus)
    worker_report_thread.submit(workReport.reportLog)



if __name__ == '__main__':
    init_work_health()
    init_blue_print()
