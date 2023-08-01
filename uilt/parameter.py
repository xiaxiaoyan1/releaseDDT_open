import re
import time
from datetime import datetime


# 自定义时间戳
def time_stamp():
    pass

# 自定义时间天数
def date_time(time_l):
    '''
    :param time_l: 自定义时间
    :return: 0:毫秒时间戳 1:unix时间戳
    '''
    Y=time_l['Y']
    M=time_l['M']
    D=time_l['D']
    h=time_l['h']
    m=time_l['m']
    s=time_l["s"]
    custom_time = datetime(Y, M, D, h, m, s)
    timestamp = custom_time.timestamp()
    return int(timestamp * 1000),int(timestamp)
# 当前时间戳
def new_time():
    '''
    :return: 0:毫秒时间戳 1:Unix时间戳
    '''
    return round(time.time() * 1000),round(time.time())
# 当前时间天数
def new_date_time():
    pass
# 访问url

def Md5_list():
    pass
def sign():
    pass

def get_parameter(key,find_data):
    '''
    :param key: 被查找关键字
    :param find_data: 备查找内容
    :return: 是否存在
    '''
    Get_parameter= str(key)
    find_data=str(find_data)
    find_key_pattern = re.escape(Get_parameter)
    find_key_data = re.search(find_key_pattern, find_data)
    return find_key_data
a={"daata":"{{time}}"}
# print(get_parameter("{{tim}}",a))
