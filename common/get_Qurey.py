
import jsonpath
import time
import re


def Get_query(x,y):
	'''
	:param x:入参变量
	:param y:上个接口的请求
	:return:正常入参参数
	'''
	global query_key,query_value
	for e in x:
		if "$" in x[e] :
			query_key = x[e].split('$')[1]
			query_value = jsonpath.jsonpath(y, '$..%s' % (query_key))
			x[e]=query_value[0]
		if query_value ==False:
			print('上一个接口响应未找到%s' % (query_key))
	return x





b={
			"channel_id": "cctv2",
			"start_time": 1688845800,
			"end_time": 1688849280,
			"channel_name": "CCTV-2财经",
			"program_name": "职场健康课-2023-26",
			"program_id": "1a1jrfm2d1ml",
			"status": 2

	}
a={
			"channel_id": "cctv2",
			"start_time": 1688845800,
			"end_time": 1688849280,
			"channel_name": "CCTV-2财经",
			"program_name": "职场健康课-2023-26",
			"program_id": "$1a1jrfm2d1ml",
			"status": 2

	}

import json
# json.dumps(b)
# a={"program_id":"$program_id","status":"$status","program_name":'',"channel_id":"cctv2"}
# Get_query(a,b)
# if '$' in a.values() or '$' in b.values():
# 	print(1)
# else:
# 	print(2)

def get_timestamp(key,query,key_word):
	'''
	:param key: 被替换内容
	:param query: 被找内容
	:param key_word: 替换内容
	:return: 正常入参参数
	'''
	for e in query:
		if key == query[e]:
			query[e]= key_word
	return query

