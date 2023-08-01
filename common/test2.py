# coding=utf-8
import json
import logging
import re
import time
from urllib.parse import unquote

import py2curl
import requests

from common import get_Qurey
from uilt import CaseAssert
from uilt.read_file import Write


def success_assert(filelist,reportpath,casename,succenum):

    resule = 'Pass'
    filelist.append(resule)  # 添加测试结果
    succenum += 1
    runtime = time.strftime('%Y-%m-%d %H:%M:%S')
    print('INFO : %s %s  result is %s' % (runtime, casename, resule))
    Write().write_excel_xls_append(reportpath, filelist)
    return  succenum
def fail_Exception_assert(filedic,filelist,a,fail_list,reportpath,i,failnum):
    failnum += 1
    filedic['result'] = a[0]
    filedic['error'] = a[1]
    filedic["openid"] = "'open_%d'" % (i - 1)
    filelist.extend(a)
    fail_list.append(filedic)
    print(a)
    Write().write_excel_xls_append(reportpath, filelist)
    return failnum
def fail_assert(resule,error,filedic,filelist,failnum,fail_list,i,res,casename,reportpath):
    a = [resule, error]
    filedic['result'] = a[0]
    filedic['error'] = a[1]
    filedic["openid"] = "'open_%d'" % (i)
    filelist.extend(a)
    fail_list.append(filedic)
    failnum += 1
    curl = py2curl.render(res.request)
    filelist[1] = curl
    filedic['curl'] = curl
    runtime = time.strftime('%Y-%m-%d %H:%M:%S')
    print('INFO : %s %s  result is %s' % (runtime, casename, resule))
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
    succenum=0
    failnum=0
    fail_list=[]
    get_respones = ''
    header={
        "uuid": "62db0038ebadb0c694a05c604c96a832",
        "deviceId": "d9e3e4e11f16d7f8",
        "ssid": "1f0a2058-de99-43c3-a821-8975cbf7fb44",
        "authorization": "TlRaa05qbGpZV0l6TnpreFpqVXpZalZtT0RkbU56ZGlNVGd4WW1aak1ETT18MTY4MzcxMDgyNDExOTY4MzQ2NHwwZjU0Yzc2YjE2OTBjZWQ5NDNkNmQzYTVhMmY4ZGZlMTNhYTQ3NzJi",
        "appid": "0990028e54b2329f2dfb4e5aeea6d625",
        "userid": "3396650614d41e599523d9df70d3ea3b",
        "hdDeviceId":"2c7a42a55688f65c0fdbea439a9b4884",
        "Content-Type": "application/json"
    }
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
        Query = unquote(filecases[8])#防转译query
        data = unquote(filecases[9])#data
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
        response=filecases[10]
        filedic = {'name': casename, 'demo': filecases[3], 'url': url, 'result': '', 'error': '','response':response,"openid":""} #错误结果列表,用于html
        filelist = [casename, url, filecases[3]]  # 测试结果列表
        Method = filecases[4]
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
            failnum += 1
            resule = 'error'
            error = '响应数据错误 : %s'%(a)
            a = [resule, error]
            filedic['result'] = a[0]
            filedic['error'] = a[1]
            filedic["openid"] = "'open_%d'"%(i-1)
            filelist.extend(a)
            fail_list.append(filedic)
            print(a)
            Write().write_excel_xls_append(reportpath, filelist)
            continue
        try:

            if Query != '' :
                Query = eval(Query)
            if data != '':
                data = eval(data)
            if get_respones != "":
                for Q in Query:
                    if "$" in Query[Q] :
                        Query = get_Qurey.Get_query(Query, get_respones)
                        '''重置依赖接口数据'''
                        get_respones = ''
                    else:
                        pass
                '''判断当前接口是否依赖上一个接口'''

                for d in data:
                    if "$" in data[d] :
                        data = get_Qurey.Get_query(Query, get_respones)
                        '''重置依赖接口数据'''
                        get_respones = ''

        except Exception as a :
            failnum +=1
            resule = 'error'
            error = '入参参数错误,请检查query或data : %s'%(a)
            a = [resule, error]
            filedic['result'] = a[0]
            filedic['error'] = a[1]
            filedic["openid"] = "'open_%d'"%(i-1)
            filelist.extend(a)
            fail_list.append(filedic)
            print(a)
            Write().write_excel_xls_append(reportpath, filelist)
            continue
        runtime = time.strftime('%Y-%m-%d %H:%M:%S')
        print('第%.f行用例'%(i),'INFO : %s  %s runing success' % (runtime,casename))
        res = ''
        if data != '' :
            data = json.dumps(data)
        if Query != "":
            data = json.dumps(data)
        try:
            session=requests.session()
            session.trust_env=False
            res=session.request(method=Method,url=url,headers=headers,params=Query,data=data,verify=False,timeout=5)
            curl = py2curl.render(res.request)
        except requests.exceptions.InvalidURL as a:
            failnum += 1
            resule = 'error'
            error='api参数错误 : %s'%(a)
            b = [resule, error]
            filedic['result'] = b[0]
            filedic['error'] = b[1]
            filedic["openid"] = "'open_%d'"%(i-1)
            filelist.extend(b)
            fail_list.append(filedic)
            print(a)
            Write().write_excel_xls_append(reportpath, filelist)
            continue
        except ValueError as a:
            failnum += 1
            resule = 'error'
            error = 'Header参数错误: %s' % (a)
            a = [resule, error]
            filedic['result'] = a[0]
            filedic['error'] = a[1]
            filedic["openid"] = "'open_%d'"%(i-1)
            filelist.extend(a)
            fail_list.append(filedic)
            Write().write_excel_xls_append(reportpath, filelist)
            continue
        except requests.exceptions.Timeout as a :
            failnum += 1
            resule = 'error'
            error = '请求超时 : %s' % (a)
            a = [resule, error]
            filedic['result'] = a[0]
            filedic['error'] = a[1]
            filedic["openid"] = "'open_%d'"%(i-1)
            filelist.extend(a)
            fail_list.append(filedic)
            Write().write_excel_xls_append(reportpath, filelist)
            print(a)
            continue
        try:
            '''获取code,判断code是否符合预期'''
            rescode = res.status_code  # 获取code码
            if code == rescode and code == 200 and response != "":
                resjson = res.json()  # 获取接口内容并以json格式展示
                '''如果code码不为200但与预期一致,就跳过断言并置为成功'''
            elif code == rescode and code != 200 and response != "":
                resule = 'Pass'
                filelist.append(resule)  # 添加测试结果
                succenum += 1
                runtime = time.strftime('%Y-%m-%d %H:%M:%S')
                print('INFO : %s %s  result is %s' % (runtime, casename, resule))
                Write().write_excel_xls_append(reportpath, filelist)
                continue
            elif code == rescode and response == "":#没有响应值判断
                resule = 'Pass'
                filelist.append(resule)  # 添加测试结果
                succenum += 1
                runtime = time.strftime('%Y-%m-%d %H:%M:%S')
                print('INFO : %s %s  result is %s' % (runtime, casename, resule))
                Write().write_excel_xls_append(reportpath, filelist)
                continue
            # 如果code码与预期不一致就跳过断言并置为失败
            else:
                resule = 'Fail'
                error = '状态码为:%d' % (rescode)
                a = [resule, error]
                filedic['result'] = a[0]
                filedic['error'] = a[1]
                filedic["openid"] = "'open_%d'"%(i)
                filelist.extend(a)
                fail_list.append(filedic)
                failnum += 1
                curl = py2curl.render(res.request)
                filelist[1] = curl
                filedic['curl'] = curl
                runtime = time.strftime('%Y-%m-%d %H:%M:%S')
                print('INFO : %s %s  result is %s' % (runtime, casename, resule))
                Write().write_excel_xls_append(reportpath, filelist)
                continue
            '''判断当前接口响应是否保存'''
            if "/" in caselever :
                get_respones=resjson
            '''断言'''
            caseassert = CaseAssert.containsassert(response, resjson)
            count = caseassert[0]  # 断言是否成功 1为成功,0为失败
            error = caseassert[1]  # 错误原因
            if count == 1:
                resule = 'Pass'
                filelist.append(resule)
                succenum += 1
                Write().write_excel_xls_append(reportpath, filelist)
                runtime = time.strftime('%Y-%m-%d %H:%M:%S')
                print('INFO : %s %s  result is %s' % (runtime, casename, resule))
            else:
                resule = 'Fail'
                a = [resule, error]
                filelist.extend(a)
                filedic['result'] = a[0]
                filedic['error'] = a[1]
                filedic["openid"] = "'open_%d'" % (i)
                failnum += 1
                runtime = time.strftime('%Y-%m-%d %H:%M:%S')
                print('INFO : %s %s  result is %s' % (runtime, casename, resule))
            if resule == 'Fail':
                curl = py2curl.render(res.request)
                filelist[1] = curl
                filedic['curl'] = curl
                filedic["openid"] = "'open_%d'" % (i)
                Write().write_excel_xls_append(reportpath, filelist)
        except Exception as a :
            '''判断4数据异常'''
            failnum += 1
            filelist = [casename, url, filecases[3],'error','用例异常%s'%(a.__traceback__.tb_lineno)]
            filedic = {'name': casename, 'curl': url, 'demo': filecases[3], 'result': 'error', 'error': '用例异常%s'%(a),'response':response,"openid":"'open_%d'"%(i)}
            fail_list.append(filedic)
            Write().write_excel_xls_append(reportpath, filelist)
            continue

        if len(filelist) == 5:
            fail_list.append(filedic)
    return succenum,failnum,fail_list
