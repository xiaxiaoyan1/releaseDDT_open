# coding=utf-8
import json
import logging
import re
import time
from urllib.parse import unquote

import py2curl
import requests

from common import get_Qurey
from uilt import CaseAssert,parameter
from uilt.read_file import Write


def success_assert(filelist,reportpath,casename,succenum):
    succenum += 1
    resule = 'Pass'
    filelist.append(resule)  # 添加测试结果
    runtime = time.strftime('%Y-%m-%d %H:%M:%S')
    print('INFO : %s %s  result is %s' % (runtime, casename, resule))
    Write().write_excel_xls_append(reportpath, filelist)
    return  succenum
def fail_Exception_assert(casename,failnum,filedic,filelist,errorcontent,reportpath,i):
    failnum +=1
    a = ['error', errorcontent]
    filedic['result'] = a[0]
    filedic['error'] = a[1]
    filedic["openid"] = "'open_%d'" % (i - 1)
    filelist.extend(a)
    print('INFO : %s%s' % (casename,errorcontent))
    Write().write_excel_xls_append(reportpath, filelist)
    return failnum

def fail_assert(error,filedic,filelist,failnum,i,res,casename,reportpath):
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
    :return: succenum: 成功数,failnum: 失败数
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
    for i in range(1,nows):
        time.sleep(0.5)
        filecases = caseexcel.row_values(i)
        Run = filecases[2]  # 是否执行
        if Run =='否' or Run == "":
            continue
        runtime = time.strftime('%Y-%m-%d %H:%M:%S')
        print('INFO : %s read file success' % (runtime))
        caselever = filecases[0]#接口等级
        casename= filecases[1]#用例名称
        #防转译
        Query=(unquote(filecases[8]))
        data = unquote(filecases[9])
        if Query != '':
            Query = eval(Query)
        if data != '':
            data = eval(data)
        '''正则匹配域名'''
        pattern = re.compile(r'^http?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        match = re.match(pattern, filecases[5])
        '''接入域名'''
        if match:
            url=filecases[5]
        else:
            url = config['appurl']
            url = '%s' % (url + filecases[5])
        code=int(filecases[6])#code码
        response=filecases[10]#响应结果
        filedic = {'name': casename, 'demo': filecases[3], 'url': url, 'result': '', 'error': '','response':response,"openid":""} #错误结果列表,用于html
        filelist = [casename, url, filecases[3]]  # 测试结果列表
        Method = filecases[4]#请求方式
        if filecases[7] == '':
            headers = header
        elif filecases[7] == '/':
            headers = ''
        else:
            headers = eval(filecases[7])
        try :
            if  response!= '':#response
                response=eval(filecases[10])#接口返回值
            else:
                response=''
        except Exception as a :
            error='用例响应数据错误 : %s'%(a)
            failnum=fail_Exception_assert(casename,failnum,filedic,filelist,error,reportpath,i)
            continue
        try:
            '''获取实时参数'''
            if Query != '' and get_response != "" and parameter.get_parameter("$",str(Query)):
                #获取上个接口字段结果
                Query = get_Qurey.Get_query(Query, get_response)
                get_response = ''
            if Query != '' and parameter.get_parameter('{{s_time}}', str(Query)) :# 毫秒时间戳
                Query = get_Qurey.get_timestamp("{{s_time}}", Query, parameter.new_time()[0])
            if Query != '' and parameter.get_parameter("{{u_time}}", str(Query)) : # unix时间戳
                Query = get_Qurey.get_timestamp("{{u_time}}", Query, parameter.new_time()[1])
            if data != '' and get_response != "" and parameter.get_parameter("$", str(data)):
                 # 获取上个接口字段结果
                data = get_Qurey.Get_query(data, get_response)
                get_response = ''
            if data != '' and parameter.get_parameter('{{s_time}}', str(data)) :# 毫秒时间戳
                data = get_Qurey.get_timestamp("{{s_time}}", data, parameter.new_time()[0])
            if data != '' and parameter.get_parameter("{{u_time}}", str(data)) : # unix时间戳
                data = get_Qurey.get_timestamp("{{u_time}}", data, parameter.new_time()[1])
        except Exception as a :
            error = '入参参数错误,请检查query或data : %s' % (a)
            failnum=fail_Exception_assert(casename,failnum,filedic, filelist, error,  reportpath, i)
            continue
        runtime = time.strftime('%Y-%m-%d %H:%M:%S')
        print('第%.f行用例'%(i),'INFO : %s  %s runing success' % (runtime,casename))
        try:
            session=requests.session()
            session.trust_env=False
            res=session.request(method=Method,url=url,headers=headers,params=Query,data=data,verify=False,timeout=5)
            curl = py2curl.render(res.request)
        except requests.exceptions.InvalidURL as a:
            error='api参数错误 : %s'%(a)
            failnum=fail_Exception_assert(casename,failnum,filedic, filelist, error, reportpath, i)
            print(curl)
            continue
        except ValueError as a:
            error = 'Header参数错误: %s' % (a)
            failnum=fail_Exception_assert(casename,failnum,filedic, filelist, error,  reportpath, i)
            print(curl)
            continue
        except requests.exceptions.Timeout as a :
            failnum += 1
            error = '请求超时 : %s' % (a)
            failnum=fail_Exception_assert(casename,failnum,filedic, filelist, error, reportpath, i)
            print(curl)
            continue
        try:
            '''获取code,判断code是否符合预期'''
            rescode = res.status_code  # 获取code码
            if code == rescode and code == 200 and response != "":
                resjson = res.json()  # 获取接口内容并以json格式展示
                '''如果code码不为200但与预期一致,就跳过断言并置为成功'''
            elif code == rescode and code != 200 and response != "":
                succenum=success_assert(filelist,reportpath,casename,succenum)
                continue
            elif code == rescode and response == "":#没有响应值判断
                succenum=success_assert(filelist,reportpath,casename,succenum)
                continue
            # 如果code码与预期不一致就跳过断言并置为失败
            else:
                error = '状态码为:%d' % (rescode)
                failnum=fail_assert(error,filedic,filelist,failnum,i,res,casename,reportpath)
                continue
            '''判断当前接口响应是否保存'''
            if "/" in caselever :
                get_response=resjson
            '''断言'''
            caseassert = CaseAssert.assert_result(response, resjson)
            count = caseassert[0]  # 断言是否成功 1为成功,0为失败
            error = caseassert[1]  # 错误原因
            if count == 1:
                succenum=success_assert(filelist,reportpath,casename,succenum)
            else:
                    failnum=fail_assert(error,filedic,filelist,failnum,i,res,casename,reportpath)
            print(response)
        except Exception as a :
            '''判断4数据异常'''
            failnum += 1
            filelist = [casename, url, filecases[3],'error','用例异常%s'%(a.__traceback__.tb_lineno)]
            filedic = {'name': casename, 'curl': url, 'demo': filecases[3], 'result': 'error', 'error': '用例异常%s'%(a),'response':response,"openid":"'open_%d'"%(i)}
            fail_list.append(filedic)
            Write().write_excel_xls_append(reportpath, filelist)
            print(curl)
            print(a)
            continue
        if len(filelist) == 5:
            fail_list.append(filedic)

    return succenum,failnum,fail_list

