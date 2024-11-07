import base64
import hashlib
import math
import os
import socket
import urllib
import pybyte as pybyte

from src.utils.Properties import pro
from src.utils.date_utils import DateUtils

MD5 = 'md5'
UTF_8 = 'utf-8'
BASE_64 = 'base64'
URL_ENCODE = 'url_encode'

def msg_encode(msg, type = BASE_64):
    encode_Str = msg
    if type == BASE_64:
        encode_Str = base64.b64encode(bytes(msg,UTF_8)).decode(UTF_8)
    elif type == MD5:
        hl = hashlib.md5()
        hl.update(msg.encode(encoding=UTF_8))
        encode_Str = hl.hexdigest()
    elif type == URL_ENCODE:
        encode_Str = urllib.request.quote(msg, safe='/:?=&', encoding='utf-8')
    return encode_Str


def msg_decode(msg, type =BASE_64):
    decode_Str = msg
    if type == BASE_64:
        decode_Str = base64.b64decode(bytes(msg,UTF_8)).decode(UTF_8)
    elif type == URL_ENCODE:
        decode_Str = urllib.request.unquote(msg)

    return decode_Str




def gb_human_read(size, dot=2):
    if 1 <= size < 1024:
        human_size = str(round(size , dot)) + 'MB'
    elif math.pow(1024, 1) <= size < math.pow(1024, 2):
        human_size = str(round(size / math.pow(1024, 1), dot)) + 'GB'
    elif math.pow(1024, 2) <= size < math.pow(1024, 3):
        human_size = str(round(size / math.pow(1024, 2), dot)) + 'TB'
    else:
        raise ValueError('{}() takes number than or equal to 0, but less than 0 given.'.format(pybyte.__name__))
    return human_size

def byte_human_read(size, dot=2):
    size = float(size)
    # 位 比特 bit
    if 0 <= size < 1:
        human_size = str(round(size / 0.125, dot)) + 'b'
    # 字节 字节 Byte
    elif 1 <= size < 1024:
        human_size = str(round(size, dot)) + 'B'
    # 千字节 千字节 Kilo Byte
    elif math.pow(1024, 1) <= size < math.pow(1024, 2):
        human_size = str(round(size / math.pow(1024, 1), dot)) + 'KB'
    # 兆字节 兆 Mega Byte
    elif math.pow(1024, 2) <= size < math.pow(1024, 3):
        human_size = str(round(size / math.pow(1024, 2), dot)) + 'MB'
    # 吉字节 吉 Giga Byte
    elif math.pow(1024, 3) <= size < math.pow(1024, 4):
        human_size = str(round(size / math.pow(1024, 3), dot)) + 'GB'
    # 太字节 太 Tera Byte
    elif math.pow(1024, 4) <= size < math.pow(1024, 5):
        human_size = str(round(size / math.pow(1024, 4), dot)) + 'TB'
    # 拍字节 拍 Peta Byte
    elif math.pow(1024, 5) <= size < math.pow(1024, 6):
        human_size = str(round(size / math.pow(1024, 5), dot)) + 'PB'
    # 艾字节 艾 Exa Byte
    elif math.pow(1024, 6) <= size < math.pow(1024, 7):
        human_size = str(round(size / math.pow(1024, 6), dot)) + 'EB'
    # 泽它字节 泽 Zetta Byte
    elif math.pow(1024, 7) <= size < math.pow(1024, 8):
        human_size = str(round(size / math.pow(1024, 7), dot)) + 'ZB'
    # 尧它字节 尧 Yotta Byte
    elif math.pow(1024, 8) <= size < math.pow(1024, 9):
        human_size = str(round(size / math.pow(1024, 8), dot)) + 'YB'
    # 千亿亿亿字节 Bront Byte
    elif math.pow(1024, 9) <= size < math.pow(1024, 10):
        human_size = str(round(size / math.pow(1024, 9), dot)) + 'BB'
    # 百万亿亿亿字节 Dogga Byte
    elif math.pow(1024, 10) <= size < math.pow(1024, 11):
        human_size = str(round(size / math.pow(1024, 10), dot)) + 'NB'
    # 十亿亿亿亿字节 Dogga Byte
    elif math.pow(1024, 11) <= size < math.pow(1024, 12):
        human_size = str(round(size / math.pow(1024, 11), dot)) + 'DB'
    # 万亿亿亿亿字节 Corydon Byte
    elif math.pow(1024, 12) <= size:
        human_size = str(round(size / math.pow(1024, 12), dot)) + 'CB'
    # 负数
    else:
        raise ValueError('{}() takes number than or equal to 0, but less than 0 given.'.format(pybyte.__name__))
    return human_size




def parse_exp(account_exp):
    start_offset = 0
    end_offset = 0
    batch_from = ''
    if account_exp.__contains__('['):
        array_1 = account_exp.split('[')

        batch_name = array_1[0].strip()
        batch_from = '[' + array_1[1]
        array_2 = array_1[1].replace(']' , '').split(':')
        start_str = array_2[0].strip()
        if start_str == '':
            start_offset = 0
        else:
            start_offset = int(start_str)

        end_str = array_2[1].strip()

        if end_str == '':
            end_offset = 0
        else:
            end_offset = int(end_str)
    else:
        batch_name = account_exp
    return (batch_name, start_offset, end_offset, batch_from)



def job_by_day(job):
    flag = False

    min = str(job['job_min']).zfill(2)
    hour = str(job['job_hour']).zfill(2)

    latest_hour_min = DateUtils.get_date_str(job['latest_exe_time']/1000, format='%H%M')
    current_hour_min = DateUtils.date_str(format='%H%M')
    target_hour_min = hour + min


    if current_hour_min != latest_hour_min and current_hour_min == target_hour_min:
        flag = True

    print('job[',job['job_name'],'] current_hour_min:', current_hour_min, ' target_hour_min:', target_hour_min, ' latest_hour_min:', latest_hour_min ,'flag:', flag)

    return flag


def job_by_week(job):
    flag = False
    # week day   1---7
    target_week_day = str(job['job_week'])
    current_day=DateUtils.date_str(format = '%Y%m%d')
    current_week_day = str(DateUtils.day_of_week_num(current_day, format ='%Y%m%d'))

    latest_day = DateUtils.get_date_str(job['latest_exe_time'] / 1000, format = '%Y%m%d')

    #判断 天 是否正确
    if current_day == latest_day or target_week_day != current_week_day:
        return False

    min = str(job['job_min']).zfill(2)
    hour = str(job['job_hour']).zfill(2)
    target_hour_min = hour + min
    current_hour_min = DateUtils.date_str(format='%H%M')

    if current_hour_min == target_hour_min:
        flag = True
    return flag


def job_by_hour(job):
    flag = False

    current_min = DateUtils.date_str(format='%M')
    target_min = str(job['job_min']).zfill(2)
    latest_min = DateUtils.get_date_str(job['latest_exe_time'] / 1000, format='%M')

    if current_min != latest_min and current_min == target_min:
        flag = True
    return flag


def job_by_only(job):
    flag = False

    current_day = DateUtils.date_str(format='%Y%m%d')

    min = str(job['job_min']).zfill(2)
    hour = str(job['job_hour']).zfill(2)
    ts = job['latest_exe_time']

    if ts != '' and ts > 0 :
        return False

    current_time = DateUtils.date_str(format='%Y%m%d%H%M')
    target_time = current_day + hour + min

    print('current_time:', current_time, ' target_time:', target_time)

    if current_time == target_time:
        flag = True
    return flag

def target_map_value(target_dict, ori_dict, k):
    if k in ori_dict:
        target_dict[k] = ori_dict[k]

project_dir=''

def project_path():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    return dir_path+'/../../'


def resource_path():
    return pro.get('resource_path')

def task_file_path():
    return pro.get('task_path')



def read_proxy_ip():
    file_path_prefix = resource_path() + 'config/'
    file_name = 'proxy_ip.csv'
    proxy_ips = []

    with open(file_path_prefix + file_name, 'r') as f:
        lst = f.readlines()
        for str in lst:
            proxy_ips.append(str)
    return proxy_ips


def local_host_ip():
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    return ip




