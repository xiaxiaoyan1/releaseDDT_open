import json
import requests
import time,datetime
import run


def sendmess(connect):#群消息推送
    url = 'https://oapi.dingtalk.com/robot/send?access_token=6d5a5ca870d603e2e5b4a954cee03c75d5ca1da4ab5ea2b8585cc95306eedd5f'
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


def sendapi(connect):#群消息推送接口自动化机器人
    url = 'https://oapi.dingtalk.com/robot/send?access_token=6d5a5ca870d603e2e5b4a954cee03c75d5ca1da4ab5ea2b8585cc95306eedd5f'
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
# send_ding()