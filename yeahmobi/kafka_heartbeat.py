#! /usr/bin/env python
# --*-- coding=utf-8 --*--

__author__ = 'jeff.yu'


import urllib2
from time import sleep



def heartBeat(timeSleep):
    print 'heart Beat running........'
    heartUrlList = ['http://172.20.0.69:8080/collector/monitor']
    while True:
        for heartUrl in heartUrlList:
            urllib2.urlopen(urllib2.Request(heartUrl))
        sleep(timeSleep)

if __name__ =='__main__':
    heartBeat(10)