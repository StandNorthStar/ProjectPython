# coding: utf-8

import redis

key = 'test-key'
host = '192.168.10.1'
red = redis.Redis(host=host, port=6379, db=4)

def getip():
    iplen = red.llen(key)
    result = {}
    for i in range(iplen):
        j = i+1
        if j < iplen:
            preip = red.lrange(name=key, start=i, end=i)[0]
            postip = red.lrange(name=key, start=j, end=j)[0]
            #print preip
            #print postip
            if preip.split('=')[0] == postip.split("=")[0]:
                if j == iplen-1:
                    result[j] = postip
                else:
                    continue
            else:
                result[i] = postip
        else:
            break
    return result
print getip()


