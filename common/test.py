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


urls=['http://img.cdn.lejiazm.com/static/resource/6df75693b6156cc7469d112aa11dd7ea.pg','http://img.cdn.lejiazm.com/static/resource/b46f60521a5dd446aed988aa91f5a902.pn','http://sh2.cdn.lejiazm.com/static/resource/1efeae6885f6503872b69e8021afb0aa.apk','http://img.cdn.lejiazm.com/static/resource/b46f60521a5dd446aed988aa91f5a902.png']
ulr=['http://img.cdn.lejiazm.com/static/resource/6df75693b6156cc7469d112aa11dd7ea.pg', 'http://sh2.cdn.lejiazm.com/static/resource/1efeae6885f6503872b69e8021afb0aa.apk', 'http://img.cdn.lejiazm.com/static/resource/b46f60521a5dd446aed988aa91f5a902.png', 'http://img.cdn.lejiazm.com/static/resource/091066bb1900b8e761f10e1c41d63d27.png', 'http://img.cdn.lejiazm.com/static/resource/c8513807ed75d11a4019b6391f1000c8.png', 'http://img.cdn.lejiazm.com/static/resource/0ef8421204d6eac6289c0a5c971ad1d2.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/a581f330f4e276357aac294b5025193b.apk', 'http://img.cdn.lejiazm.com/static/resource/db15fb362ed07e83819955d4484d9f89.jpg', 'http://img.cdn.lejiazm.com/static/resource/a99045239ec62e3504a0d1e81c67cc9c.jpg', 'http://img.cdn.lejiazm.com/static/resource/577167ab8d1ade8039331b867a56fadc.png', 'http://img.cdn.lejiazm.com/static/resource/c2bf813f7c4858cd7e0e54aeb614959a.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/3b446986a1e4cf793e68512f4937085e.apk', 'http://img.cdn.lejiazm.com/static/resource/ab1a2fc2a342e85815cbd7596a9a6cdc.jpg', 'http://img.cdn.lejiazm.com/static/resource/b90a7f25d5b14716f27148c5c2f84148.jpg', 'http://img.cdn.lejiazm.com/static/resource/a13ba78b843ca3c4090f8c020a7579dd.png', 'http://img.cdn.lejiazm.com/static/resource/c8b362910e27eccd83b668c3e69fb609.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/7f4ca011891c17d91fbd31c01065de12.apk', 'http://img.cdn.lejiazm.com/static/resource/328b570dfb864d121e4d5b913cb885d1.jpg', 'http://img.cdn.lejiazm.com/static/resource/b48f4cc8bd4a4a61d3f5a9a10f27498d.jpg', 'http://img.cdn.lejiazm.com/static/resource/afcca612fffe73a6158b60f92e7ec530.png', 'http://img.cdn.lejiazm.com/static/resource/bad1df58cc9bfabd44423c953056f6af.png', 'http://sh2.cdn.lejiazm.com/static/resource/1ad6b945d2d582bb6e509193530b0427.apk', 'http://img.cdn.lejiazm.com/static/resource/862e18d9ab0b3589303e1c763744df0d.png', 'http://img.cdn.lejiazm.com/static/resource/bad1df58cc9bfabd44423c953056f6af.png', 'http://sh2.cdn.lejiazm.com/static/resource/e85cb02d6d3e9d2691c819eee0d0d987.apk', 'http://img.cdn.lejiazm.com/static/resource/4c4e92e96dea72770ef745ef0700ef3a.jpg', 'http://img.cdn.lejiazm.com/static/resource/53429eea7d4df3688847985dc15cdee8.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/4c5914acab67f2a9dfb015f9aa040ebb.apk', 'http://img.cdn.lejiazm.com/static/resource/fa12bb7d2f970ea11253ebdc8fb5386b.png', 'http://img.cdn.lejiazm.com/static/resource/445bb4d5623aadae9700ec1890e73844.png', 'http://sh2.cdn.lejiazm.com/static/resource/fb04ec10e5d0bb447d4ed8a3363baeaa.apk', 'http://img.cdn.lejiazm.com/static/resource/4dbe94791e34079ad56af431e71f671f.png', 'http://img.cdn.lejiazm.com/static/resource/92a1a1193f0b1427852a3888b479feff.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/00a8d16e7a80a34cebbd2aaa8c2c3720.apk', 'http://img.cdn.lejiazm.com/static/resource/83f5031acd40064acb8d1e1a13f60d72.png', 'http://img.cdn.lejiazm.com/static/resource/49510249f29172aa7b8de67bf3672886.jpg', 'https://vd4.bdstatic.com/mda-pgdc0925f6x6m7zg/720p/h264/1689323338997673849/mda-pgdc0925f6x6m7zg.mp4', 'http://sh2.cdn.lejiazm.com/static/resource/3b446986a1e4cf793e68512f4937085e.apk', 'http://img.cdn.lejiazm.com/static/resource/940e958c2ceb5951e49c71fd0e7ccd4b.png', 'http://img.cdn.lejiazm.com/static/resource/92ad40d286015a373c42e2062feaf752.jpg', 'https://vd4.bdstatic.com/mda-pgdfsgimy4qq1pjq/720p/h264/1689332905295314154/mda-pgdfsgimy4qq1pjq.mp4', 'http://sh2.cdn.lejiazm.com/static/resource/00a8d16e7a80a34cebbd2aaa8c2c3720.apk', 'http://img.cdn.lejiazm.com/static/resource/80d7597e3cb4613a75ba5c01fa9d2d02.png', 'http://img.cdn.lejiazm.com/static/resource/e0cb3ac7d7fc526e12bd70136c47b89d.jpg', 'https://vd2.bdstatic.com/mda-pgdddt1y7wkq7r1t/720p/h264/1689326971208102123/mda-pgdddt1y7wkq7r1t.mp4', 'http://sh2.cdn.lejiazm.com/static/resource/3b446986a1e4cf793e68512f4937085e.apk', 'http://img.cdn.lejiazm.com/static/resource/d212ca1b92fca063126648c36280bde0.png', 'http://img.cdn.lejiazm.com/static/resource/5f5068488ddb277e8d1c5d15b575662b.png', 'https://vd2.bdstatic.com/mda-pgdcpprmqjj8k2x4/720p/h264/1689325116590169050/mda-pgdcpprmqjj8k2x4.mp4', 'http://sh2.cdn.lejiazm.com/static/resource/3b446986a1e4cf793e68512f4937085e.apk', 'http://img.cdn.lejiazm.com/static/resource/9f23dfeaad0c4846f235050f9cb6a606.png', 'http://img.cdn.lejiazm.com/static/resource/20da9af4435b0e537e4564b1da4d804c.png', 'http://sh2.cdn.lejiazm.com/static/resource/00a8d16e7a80a34cebbd2aaa8c2c3720.apk', 'http://weixin.qq.com/r/DhA2LsDEp53YrYRN90Uc', 'https://qm.qq.com/cgi-bin/qm/qr', 'http://img.cdn.lejiazm.com/static/resource/11eed5f9f696cff38f68d867163e640e.png', 'http://sh2.cdn.lejiazm.com/static/resource/846798ceb2dc4685b310460e75526c28.apk', 'http://img.cdn.lejiazm.com/static/resource/e24c183808236449ffcb0b2c9cccd0d6.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/3b446986a1e4cf793e68512f4937085e.apk', 'http://img.cdn.lejiazm.com/static/resource/da92d211653d011e7fd9ab081df4b057.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/db3d52ce7ef8801d676354629cd54aab.apk', 'http://img.cdn.lejiazm.com/static/resource/2d0e22b646dbe974c10e3873fe83162f.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/4c5914acab67f2a9dfb015f9aa040ebb.apk', 'http://img.cdn.lejiazm.com/static/resource/6582fed5cb21170a2f2077171b5e3d43.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/8d2aae6157a8de67f89e415e5cafb474.apk', 'http://img.cdn.lejiazm.com/static/resource/e135969749674ec1908e33420a0a38e7.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/3baf11cfb1dee7738910e09e94779053.apk', 'http://img.cdn.lejiazm.com/static/resource/d5073ac9f9d29bf317f226cad393d39a.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/57199dc0b65b8260ced439ae283eb50e.apk', 'http://img.cdn.lejiazm.com/static/resource/154582b5981922ded03374c2b632b4e9.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/a581f330f4e276357aac294b5025193b.apk', 'http://img.cdn.lejiazm.com/static/resource/18cca0a8025c96455b45e927ecfe6025.png', 'http://sh2.cdn.lejiazm.com/static/resource/00a8d16e7a80a34cebbd2aaa8c2c3720.apk', 'http://img.cdn.lejiazm.com/static/resource/041aa4d935165d63ec6dba3880fa2292.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/283b6ad9b5e7bc59d7a99d2cdc15acbf.apk', 'http://img.cdn.lejiazm.com/static/resource/245d15e61fe5fbffb7bb208204e7b059.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/7f4ca011891c17d91fbd31c01065de12.apk', 'http://img.cdn.lejiazm.com/static/resource/d08ca328443207f9047b544f4534ba12.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/39665c91a361095a0083e21df20efe0d.apk', 'http://img.cdn.lejiazm.com/static/resource/3ff3c97b24d5ec3f12d91b61f3ca5f61.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/6feaa3066c23565d1414155a151a2bb8.apk', 'http://img.cdn.lejiazm.com/static/resource/430494de6d30fa5f09c22f61dd18e4ab.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/1774b45a317e033e4d7976d6f024f8b4.apk', 'http://img.cdn.lejiazm.com/static/resource/174a3954773db02fba461b445ed68ef5.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/5b1026a5b17503b2b8b8783ae46d5b95.apk', 'http://img.cdn.lejiazm.com/static/resource/455d6bcd512084cd3d572478c70f1b58.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/bfaa2e28ed59a3605b1ea7d87fde3d47.apk', 'http://img.cdn.lejiazm.com/static/resource/8de83ee76300825918849ccb49e82487.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/467530c26ad79bccc0b64e6372358881.apk', 'http://img.cdn.lejiazm.com/static/resource/40e72688b09de5e4f67e5c5bc54ae8c6.png', 'http://img.cdn.lejiazm.com/static/resource/8f45ad903d2c598d3c9f75ce5aab271f.jpg', 'http://sh2.cdn.lejiazm.com/static/resource/b44b0956811487a77124f0b12bb73f5a.apk']

# print(dis.dis(multi_threaded_requests))



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
        elif type(test_result[key]) != type(api_value[0]) or check_list_type(api_value)==False:
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
a={
    "errCode": 0,
    "data": [
        {
            "code": "cctv5plus",
            "name": "CCTV-5+体育赛事",
            "channelNum": 18
        }]}
b={
    "errCode": 0,
    "data": [
        {
            "code": "kb-cctv1",
            "name": "CCTV-1综合",
            "channelNum": 1
        },
        {
            "code": "kb-cctv2",
            "name": "CCTV-2财经",
            "channelNum": 2
        },
        {
            "code": "cctv5plus",
            "name": "CCTV-5+体育赛事",
            "channelNum": 18
        }
    ]}

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
 # 测试示例
json_str1 ='''
{"errCode":0,"channelCode":"zj-qingyunian","deviceMask":2}
'''
json_str2 = '''
{"errCode":0,"data":{"quit":[{"contentType":1,"bgPicUrl":"http://cdn4.dianshihome.com/static/ad/19518ea5a2554c051408bc82de621e20.jpg","apkUrl":"http://cdn4.dianshihome.com/static/apk/319272cad7062b30933837d4f1ff8aa8.apk","apkName":"com.cibn.tv","apkMD5":"319272cad7062b30933837d4f1ff8aa8","apkSize":17875706,"jump":{"type":1,"value":{"channelCode":"zj-qingyunian"}},"deviceMask":2}]}}
'''







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