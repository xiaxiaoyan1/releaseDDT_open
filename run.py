from Config.Config_dic import *
from common import apisend
from uilt import read_file, get_dingtalk
from uilt.read_file import Write
from common import RunHtml
import time,datetime
import sys

def Run(configFile,Sheet):
    # try:
    t = time.time()
    date_stamp = datetime.datetime.fromtimestamp(t)
    sendtime = datetime.datetime.strftime(date_stamp, "%H%M")
    startdata = time.strftime('%Y-%m-%d %H:%M:%S')
    '''读取配置文件'''
    configlist = config_file(configFile)#读取配置文件中用例表
    file = configlist['casefile']
    # sheet = configlist['sheetname']#读取配置文件中表格名
    sheet = Sheet
    run_project = configlist['project']#执行项目
    report_file=configlist['report_file']
    senddingding = configlist['senddingding']#发送钉钉
    reportpath = Write().WriteNewfile(report_file,sheet)#创建报告表
    casefilecon = read_file.ReadFile(file, sheet)#读取用例数据
    casefile = casefilecon[0]
    nows = casefilecon[1]
    version = casefilecon[2]
    runtime = time.strftime('%Y-%m-%d %H:%M:%S')
    print('INFO : %s read %s,%s,%s ' % (runtime, casefile,nows,version))
    #执行接口用例
    count = apisend.Common(casefile, nows, reportpath,configlist)
    stopdata = time.strftime('%Y-%m-%d %H:%M:%S')
    succenum = count[0]
    failnum = count[1]
    fail_list = count[2]
    countnum = succenum+failnum
    counts ='%.2f'%(succenum*100/countnum)
    time_list = {'start_time': startdata, 'end_time': stopdata}
    versiondic = {'version':version,'pass_rate':'%s'%(counts)+"%",'ispass':succenum,'isfail':failnum}
    # content=RunHtml.htmlresport(fail_list=fail_list, timelist=time_list, versiondic=versiondic)
    reportTime = datetime.datetime.strftime(date_stamp, "%Y%m%d%H%M")
    # with open("HtmlReport%s.html" % (reportTime), 'w') as ch:
    #     ch.write(content)

    get_dingtalk.sendapi("%s-本次运行结果:"%(run_project) +
                         "\n" + "成功：%s" % (succenum) +
                         "\n" + "失败：%s" % (failnum) +
                         "\n" + "报告：http://47.93.62.235/%s/%s-Report%s.html" % (run_project, sheet, reportTime) +
                         "\n" + "详细报告：http://47.93.62.235/%s/%s-测试报告.xls" % (run_project, sheet))
    # print("%s-本次运行结果:"%(run_project) +
    #                      "\n" + "成功：%s" % (succenum) +
    #                      "\n" + "失败：%s" % (failnum) +
    #                      "\n" + "报告：http://47.93.62.235/%s/%s-Report%s.html" % (
    #                      run_project, Sheet, reportTime) +
    #                      "\n" + "详细报告：http://47.93.62.235/%s/%s测试报告.xls"% (run_project, Sheet))
    # # except Exception as a:
    #     get_dingtalk.sendmess("执行异常:")
    #     print(a)

if __name__=='__main__':
    Run("config_file2","Sheet2")
    # Run(sys.argv[1],sys.argv[2])