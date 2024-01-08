# coding=utf-8
import logging
import re
import time
from urllib.parse import unquote

import py2curl
import requests

from common import get_Qurey
from uilt import CaseAssert, parameter
from uilt.read_file import Write


def success_assert(filelist,reportpath,casename,succenum):
    '''

    :param filelist:报告列表
    :param reportpath:报告路径
    :param casename:用例名称
    :param succenum:成功次数
    :return:成功次数
    '''
    succenum += 1
    resule = 'Pass'
    filelist.append(resule)  # 添加测试结果
    runtime = time.strftime('%Y-%m-%d %H:%M:%S')
    print('INFO : %s %s  result is %s' % (runtime, casename, resule))
    Write().write_excel_xls_append(reportpath, filelist)
    return  succenum
def fail_Exception_assert(casename,failnum,filedic,filelist,errorcontent,reportpath,i):#异常判断
    '''

    :param casename:用例名称
    :param failnum:失败次数
    :param filedic:失败用例用于html
    :param filelist:报告列表
    :param errorcontent:错误内容
    :param reportpath:报告路径
    :param i:行数
    :return:错误次数
    '''
    failnum +=1
    a = ['error', errorcontent]
    filedic['result'] = a[0]
    filedic['error'] = a[1]
    filedic["openid"] = "'open_%d'" % (i - 1)
    filelist.extend(a)
    print('INFO : %s%s' % (casename,errorcontent))
    Write().write_excel_xls_append(reportpath, filelist)
    return failnum

def fail_assert(error,filedic,filelist,failnum,i,res,casename,reportpath):#错误判断
    '''

    :param error:错误原因
    :param filedic:错误列表用于html
    :param filelist:用例列表
    :param failnum:错误次数
    :param i:用例行数
    :param res:接口响应
    :param casename:用例名称
    :param reportpath:报告路径
    :return:错误次数
    '''
    failnum += 1
    a = ['Fail', error]
    filedic['result'] = a[0]
    filedic['error'] = a[1]
    filedic["openid"] = "'open_%d'" % (i)
    filelist.extend(a)
    curl = py2curl.render(res.request)
    filelist[1] = curl
    filedic['curl'] = curl
    runtime = time.strftime('%Y-%m-%d %H:%M:%S')
    print(curl)
    print(error)
    print('INFO : %s %s  result is %s' % (runtime, casename, 'fail'))
    Write().write_excel_xls_append(reportpath, filelist)
    return failnum


def Common(caseexcel,nows,reportpath,config):
    '''
    :param caseexcel: 测试用例路径信息
    :param nows: 用例行数
    :param reportpath: 测试报告路径
    :return: 0: 成功数 1: 失败数 2: 失败列表
    '''
    logging.basicConfig(filename='log_record.txt',
                        level=logging.DEBUG, filemode='w', format='[%(asctime)s] [%(levelname)s] >>>  %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S')
    global curl, Query, data
    succenum=0
    failnum=0
    fail_list=[]
    get_response = ''
    header= eval(config["header"])
    '''读取表格测试用例,各参数赋值'''

    #此处后还有代码
    return succenum,failnum,fail_list

