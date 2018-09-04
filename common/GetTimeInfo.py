# -*- coding:utf8 -*-

__author__ = "杨果"

import time

def gettime():
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    return nowtime

def getday():
    day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    return day

def getdate(days=0):
    nowdate = time.strftime("%Y-%m-%d", time.localtime(time.time()-60*60*24*int(days)))
    return nowdate

if __name__ == "__main__":
    print(gettime())
    print(getday())
    print(getdate())
