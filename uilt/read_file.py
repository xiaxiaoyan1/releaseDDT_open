
# coding=utf-8
import xlrd,time  #xlrd是1.2.0的版本，高版本执行会有问题
import os
import xlwt
from xlwt import *
from xlutils.copy import copy
def ReadFile(file,sheet_name):
    '''

    :param file: 测试用例文件路径
    :param sheet_name: 表格名称
    :return: 文件读取数据,用例行数,表格名称
    '''

    '''读取excel表格内容并返回表格路径数据'''
    opxl=xlrd.open_workbook(file)
    optext=opxl.sheet_by_name(sheet_name)#获取指定名称表
    nows=optext.nrows#获取表格行数
    runtime = time.strftime('%Y-%m-%d %H:%M:%S')
    # print('INFO : %s read %s' % (runtime,file))
    return optext,nows,sheet_name
class Write():
    def WriteNewfile(self,report_file,sheetname):
        '''创建excel表格并规定表格样式'''
        flie=Workbook(encoding='utf8')
        table=flie.add_sheet('测试结果')
        casename_col = table.col(0)  #设置需要修改的单元格,设置整列
        casename_col.width = 256 * 35  #设置宽度
        url_col = table.col(1)
        url_col.width = 256 * 70
        demon_col = table.col(2)
        demon_col.width = 256 * 20
        resule_col = table.col(3)
        resule_col.width = 256 * 10
        error_col = table.col(4)
        error_col.width = 256 * 70
        patter = easyxf('pattern: pattern solid, fore_colour gold; font: bold on,height 240')#设置首行单元格背景样式
        table.write(0,0,'用例名称',patter)
        table.write(0,1,'接口url',patter)
        table.write(0,2,'模块',patter)
        table.write(0,3,'执行结果',patter)
        table.write(0,4,'错误返回',patter)
        execlfile='%s'%(sheetname)+'测试报告'+'.xls'#获取当前时间并给表格命名
        dis = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),report_file)#项目管理器运行
        filelpath = os.path.join(dis, execlfile)
        flie.save(filelpath)
        runtime = time.strftime('%Y-%m-%d %H:%M:%S')
        return filelpath
    def write_excel_xls_append(self,filepath,filelist):
        '''
        :param filepath: 文件路径
        :param filelist: 写入数据
        :return:None
        '''
        workbook = xlrd.open_workbook(filepath,formatting_info=True)  # 打开工作簿,并保存原有数据样式
        runtime = time.strftime('%Y-%m-%d %H:%M:%S')
        worksheet = workbook.sheet_by_name('测试结果')  # # 获取工作簿中所有表格中的的第一个表格(第一个sheet页)
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        runtime = time.strftime('%Y-%m-%d %H:%M:%S')
        new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格(第一个sheet页)
        error_style = xlwt.easyxf('pattern: pattern solid, fore_colour red; font: bold on')
        for j in range(0, len(filelist)):
            if len(filelist) == 5:
                '''fail数据追加'''
                new_worksheet.write(rows_old, j, filelist[j],error_style)  # 追加写入数据，注意是从i+rows_old行开始写入
            else:
                '''pass数据追加'''
                new_worksheet.write(rows_old, j, filelist[j])
        runtime = time.strftime('%Y-%m-%d %H:%M:%S')
        new_workbook.save(filepath)  # 保存工作簿8
        runtime = time.strftime('%Y-%m-%d %H:%M:%S')
