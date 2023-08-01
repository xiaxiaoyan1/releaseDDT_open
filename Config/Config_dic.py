import os

def ReadConfig(config_file) :
    configfile = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config_file)
    with open(configfile, 'rb') as b:
        a=b.read().decode('utf-8')
        return a
def split_file(config_file):
    a =ReadConfig(config_file)
    body=a.split('\r')
    dic=[]
    for i in range(len(body)):
        a=body[i].split(' = ')
        for j in range(len(a)):
            dic.append(a[j])
    return dic
def split_data(data):
    for i in range(0,len(data)):
        print(data[i])
        data = data[i].replace("'",'"')
    return data
def config_file(config_file):
    a=split_file(config_file)
    '''将文件内容转化为字典'''
    config={
    'appurl':a[2],
    'cmsURL':a[4],
    'casefile':a[6],
    'sheetname':a[8],
    'project':a[11],
    'senddingding':a[13],
    'header':a[15],
    'report_file':a[17]
    }

    return config
# print(config_file("config_file"))