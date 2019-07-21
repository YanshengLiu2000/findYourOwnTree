# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
import json
import CONFIG
# reload(sys)
# sys.setdefaultencoding('utf-8')

YOUDAO_URL = 'http://openapi.youdao.com/api'
APP_KEY = CONFIG.APP_KEY
APP_SECRET = CONFIG.APP_SECRET


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(quest):
    # q = "test"
    q=quest
    data = {}
    data['from'] = 'EN'
    data['to'] = 'zh-CHS'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)

    # print(response.content.decode())
    return response.content.decode()

def getAllMeanings(word):
    res=json.loads(connect(word))
    # meanings=res['web'][0]['value']
    meanings=[]
    try:
        for item in res['web']:
            meanings+=item['value'][:]#dont need add every meanings in this item['value'], valueable meanings are res['web'][0]
    except:
        pass
    # print('TEST in get AllMeanings: meanings=',meanings)
    # print()
    # print(res['basic']['explains'])
    extra_meaning=[]
    try:
        for str in res['basic']['explains']:
            extra_meaning+=str.replace('.','，').replace('；','，').replace('。','，').strip(' ').split('，')
    except:
        pass
    n=0
    while n<len(extra_meaning):# pop [v,n,adj,adv]
        if '\u4e00'<=extra_meaning[n]<='\u9fff':# check if Chinese
            n+=1
        else:
            extra_meaning.pop(n)
    print("TEST in {} get All MEANINGS: extra_meaning={}".format(word,extra_meaning))
    return meanings+extra_meaning


if __name__ == '__main__':
    # res=connect('test')
    #===============================================
    # print(type(res))
    # print(res)
    # j=json.loads(res)
    # print('==============================')
    # # print(j)
    # print(type(j))
    # print(j['web'])
    # print(j['basic'])
    # print('=============TEST======================')
    # meanings=[]
    # for item in j['web']:
    #     print(item['value'],end=' ')
    # print('========')
    # print(j['basic']['explains'])
    print(getAllMeanings('apple'))