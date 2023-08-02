import json
import requests

def sendUI(connect):#群消息推送UI自动化机器人
    url = 'https://oapi.dingtalk.com/robot/send?access_token=6d5a5ca870d603e2e5b4a954cee03c75d5ca1da4ab5ea2b8585cc95306eedd5f'#测试本地钉钉
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    post_data = {
        "msgtype": "text",
        "text": {
            "content": "%s"%(connect)
        },
        "at": {
            "atUserIds": ["10093530"],
        }
    }
    r = requests.post(url, headers=headers, data=json.dumps(post_data))
    print(r.content)
def sendapi(connect):#群消息推送接口自动化机器人
    url ='https://oapi.dingtalk.com/robot/send?access_token=9fea6d929611a6533d62bdbaa7d0baecb09bcea835bdc729585d221fa88242ea'
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    post_data = {
        "msgtype": "text",
        "text": {
            "content": "%s"%(connect)
        },
        "at": {
            "atUserIds": ["10093530"],
        }
    }
    r = requests.post(url, headers=headers, data=json.dumps(post_data))
    print(r.content)