import requests


from src.utils import tools_utils
from src.utils.date_utils import DateUtils


def testHost():
    print('testHost............................')
    realUrl = 'http://192.168.2.27:27777'
    rsp = requests.get(realUrl)

    print(rsp.text)

def testRunJob():
    host = tools.local_host_ip()
    print(host)
    url = 'http://127.0.0.1:27777/server/workerHeartbeat'
    print('url:'+ url)
    ts = DateUtils.get_timestamp()
    myobj = {"appId": 1, "appName": "python_app", "client": "KingPenguin", "containerInfos": [],
             "heartbeatTime": ts, "heavyTaskTrackerNum": 0, "lightTaskTrackerNum": 0, "overload": 'false',
             "protocol": "HTTP",
             "systemMetrics": {"cpuLoad": 2.3032, "cpuProcessors": 20, "diskTotal": 875.2685, "diskUsage": 0.124,
                               "diskUsed": 108.5645, "jvmMaxMemory": 7.748, "jvmMemoryUsage": 0.0056,
                               "jvmUsedMemory": 0.0432, "score": 87},
             "version": "UNKNOWN", "workerAddress": ''}

    rsp = requests.post(url, json=myobj)
    print('reportHealth.....', rsp.status_code)




testHost()



