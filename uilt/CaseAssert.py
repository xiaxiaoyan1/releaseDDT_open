import concurrent.futures
import json
import re,requests

import jsonpath
import dis
def equal_to(element,list):
    assert_element=element in list
    if assert_element == True:
        return True
    else:
        return False


# 判断返回数据的url是否正确
def find_urls(json_data) :  #查找数据中所有的url
    # 定义URL的正则表达式模式
    json_data=json.dumps(json_data)
    pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w .-]*/?')
    # 将JSON数据解析为Python对象
    # json_data = json.loads(json_data)
    # 查找所有的URL
    urls = re.findall(pattern,json_data)
    return urls

def send_urls(json_data): #请求url是否正确
    global result_url_code
    count=0
    fail_url = []
    urls=find_urls(json_data)
    if urls ==[]:
        count=1
    else:
        for url in urls:
            if "lejiazm" in url and "apk"in url :
                result_url_code=200
            else:
                result_url_code=requests.get(url).status_code
            if result_url_code == 200:
                count=1
            else:
                fail_url.append(url)
                count=0
                break
    return count,fail_url



def check_list_type(lst):
    if lst == []:
        return True
    else:
        data_type = type(lst[0])
        return  all(isinstance(item,data_type) for item in lst)

def containsassert(test_result,api_result):
    '''
    :param test_result: 预期结果
    :param api_result: 接口响应数据
    :return: 断言结果,错误结果
    '''
    #count = 0  断言结果 1为成功,0为失败
    global result,key,api_value
    count=0
    if type(test_result) in (int,str):
        equal = equal_to(test_result, api_result)
        if equal == True:
            count = 1
            return count
        else:
            count = 0
            return count
    for key in test_result:
        if test_result[key] is None :
            test_result[key]='null'
        api_value = jsonpath.jsonpath(api_result, '$..%s' % (key))  # 用键匹配接口内容对应数据,False为无对应键数据
        if api_value == False:#预期键不存在
            api_value = "不存在"
            count=0
            break
        elif api_value[0] is None:
            api_value[0]="null"
        elif type(api_value[0]) == int and test_result[key] in ("",{},[]):
            '''如果模糊校验int类型的字段,直接为空就通过'''
            count=1
            continue
        elif type(test_result[key]) != type(api_value[0]) :
            '''预期值与实际值类型不一致'''
            api_value="%s类型错误"%(api_value[0])
            count=0
            break
        elif test_result[key] in ("",[],{}) :
            '''非int类型值为空,直接判断返回内容类型是否相'''
            '''{'product':''}'''
            if  type(test_result[key])== type(api_value[0]):
                count = 1
                continue
            else:
                count =0
                break
        elif type(test_result[key]) in (str,int):
            '''如果值str和int直接判断是否相等'''
            equal = equal_to(test_result[key], api_value)
            if equal == True:
                count = 1
                continue
            else:
                count = 0
                break

        elif type(test_result[key])==list :

            if type(test_result[key][0]) in (int,str) :#如果字段结果是字符串或者数字格式再次递归对比
                if set(test_result[key]).issubset( api_result[key]):
                    count = 1
                    continue
                else:
                    count = 0
                    break

            else:#如果字段结果是列表和字典格式再次递归对比
                re = containsassert(test_result[key][0], api_result[key])
                if re == 1:
                    count = 1
                    continue
                else:
                    count = 0
                    break
        elif type(test_result[key]) == dict:
            '''如果是字段的结果是字典再次递归对比'''
            re = containsassert(test_result[key], api_result[key])
            if re==1:
                count=1
                continue
            else:
                count=0
                break
        else:
            count=3
            break

    return count
def assert_result(json1,json2):
    global assert_a,count
    json1=dict(json1)
    json2=dict(json2)
    lis=containsassert(json1, json2)
    assert_a=lis
    errnoresult=''
    if assert_a == 1:
        # url_result = visit_urls(json2)# 查找返回数据中存在url,如果存在,判断url是否200
        # if url_result[0]==1:
        #     count=1
        # else:
        #     errnoresult = "URL地址错误:%s" % (url_result[1])
        #     count=0
        count=1
    elif assert_a == 0:
        count=0
        errnoresult = "预期:%s" % (str(json1)) +"   实际:{%s:%s}"% (key,str(api_value))
    else:
        count=0
        errnoresult = "断言异常%s" % (str(json1))

    return count, errnoresult


# print(assert_result(a,b))
'''比较两个JSON结构是否相同'''
def compare_json(json1, json2):
    # 检查数据类型是否相同
    if type(json1) != type(json2):
        return False
     # 如果是字典类型，则递归比较键和值
    if isinstance(json1, dict):
        if type(json1) != type(json2):
            return False
        for key in json1:
            if key not in json2:
                return False
            if type(json1[key] ) in (str,int) and type(json1[key])== type(json2[key]):
                continue
            elif not compare_json(json1[key], json2[key]):
                return False
     # 如果是列表类型，则递归比较每个元素
    elif isinstance(json1, list):
        if len(json1) == 0 and type(json1)== type(json2):
            return True
        for i in range(len(json1)):
            if not compare_json(json1[i], json2[i]):
                return False
     # 其他类型直接比较值
    else:
        if type(json1) != type(json2):
            return False
    return True








#判断返回数据的所有url是否正常
def visit_urls(url_list):
    count = 1
    fail_url = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(check_url, url) for url in url_list]#遍历所有url生成线程并提交到线程池
        for future in concurrent.futures.as_completed(futures):#遍历所有url请求结果
            result = future.result()
            if result[0] == 0:
                count = 0
                fail_url.append(result[1])
                # executor.shutdown(wait=False)#停止所有线程
                # break
    return count,fail_url
def check_url(url):
    try:
        '''乐家的apk不做判断'''
        if "lejiazm" in url and "apk" in url:
            return 1,url
        else:
            response = requests.get(url)
        if response.status_code == 200:
            return 1,url
        else:
            return 0,url
    except requests.exceptions.RequestException:
        return 0,url