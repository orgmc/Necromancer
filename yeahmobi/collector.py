#! /usr/bin/env python

import time
import thread
import os
import urllib2
import urllib
import time
import sys
from random import choice
from string import letters,digits


count = 0

def mutiChoice(maxCount):
    returnStr = ''
    selectLetters = letters + digits
    for i in range(maxCount):
        returnStr += choice(selectLetters)
    return returnStr

def genTransactionId():
    return '{0}-{1}-{2}-{3}-{4}'.format(mutiChoice(8), mutiChoice(4), mutiChoice(4), mutiChoice(4), mutiChoice(12))


def mockYeahmobi(sleeptime):
    ISOTIMEFORMAT='%Y-%m-%d %X'
    global count
    while True:
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', count
        data = {'collector_param':{"aff_id":"19900305"+str(choice(range(1, 100000))),"aff_manager":str(choice(range(1, 100000))),"aff_sub1":"affsub","aff_sub2":"affsub2","aff_sub3":"affsub3","aff_sub4":"affsub4","aff_sub5":"affsub5","aff_sub6":"affsub6","aff_sub7":"affsub7","aff_sub8":"affsub8","adv_id":str(choice(range(1, 1000000))),"adv_manager":"0","adv_sub1":"affsub","adv_sub2":"advsub2","adv_sub3":"advsub3","adv_sub4":"advsub4","adv_sub5":"advsub5","adv_sub6":"advsub6","adv_sub7":"advsub7","adv_sub8":"advsub8","offer_id":str(choice(range(1, 100000))),"currency":"GBP","rpa":"20.0","cpa":"15.0","click_ip":"54.86.55.142","conv_ip":"54.86.55.142","transaction_id":genTransactionId(),"click_time":time.strftime(ISOTIMEFORMAT, time.localtime()),"conv_time":time.strftime(ISOTIMEFORMAT, time.localtime()),"user_agent":"Mozilla/5.0+(iPhone;+U;+CPU+iPhone+OS+4_3_2+like+Mac+OS+X;+zh-cn)+AppleWebKit/533.17.9+(KHTML+like+Gecko)+Version/5.0.2+Mobile/8H7+Safari/6533.18.5","browser":"1","device_model":"1","os_ver":"0","country":"ZZ","log_type":choice(("1", "0")),"visitor_id":"3274c4c8-0f0c-4517-8956-77eef6a21d83","forward_ips":"127.0.0.1","state":"-1","city":"-1","isp":"-1","mobile_brand":"-1","platform_id":"","screen_width":"320","screen_height":"480","conversions":"","track_type":"0","session_id":"e97f1f87-7a08-4b0a-8465-02bf53c5685f","visitor_node_id":"ubuntu-template","expiration_date":"2014-12-05","is_unique_click":"1","gcid":"","gcname":"","browser_name":"Mobile+Safari","device_brand_name":"Apple","device_brand":"1","device_model_name":"iPhone","device_type_name":"Mobile","device_type":"1","platform_name":"iOS","os_ver_name":"4.3.2","ref_conv_track":"http://www.65536_conv_07081624.com","referer":"http://www.65536_click_1913.com"},'platformName':'yfnormalpf'}
        postdata = urllib.urlencode(data)
        rsp = urllib2.build_opener().open(urllib2.Request('http://172.20.0.69:8080/collector/collector?', postdata)).read()
        time.sleep(sleeptime)
        count += 1
    thread.exit_thread()

def mockTradingdesk(sleeptime):
    ISOTIMEFORMAT='%Y-%m-%d %X'
    global count
    while True:
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', count
        data = {'collector_param':{"time_stamp":time.strftime(ISOTIMEFORMAT, time.localtime()),"click_id":"td_test","campaign_id":"3","offer_id":"4","ref_site":"5","site":"6","click_time":"7","cost_per_click":"8","payout":"9","real_ip":"10","proxy_ip":"11","device_id":"12","os_id":"13","carrier_id":"14","mobile_brand_id":"15","screen_h":"16","screen_w":"17","screen_id":"18","city_id":"19","brand_id":"20","model_id":"21","country_id":"22","state_id":"23","conversion_time":"24","event":"25","sub1":"26","sub2":"27","sub3":"28","sub4":"29","sub5":"30","sub6":"31","sub7":"32","sub8":"33","click":"34","lp_click":"35","conversion":"36","sub_campaign_id":"37"},'platformName':'hbtradingdesk01'}
        postdata = urllib.urlencode(data)
        rsp = urllib2.build_opener().open(urllib2.Request('http://172.20.0.69:8080/collector/collector?', postdata)).read()
        time.sleep(sleeptime)
        count += 1
    thread.exit_thread()

def testYM(threadnum): #Use thread.start_new_thread() to create 2 new threads
    for i in range(threadnum):
        thread.start_new_thread(mockYeahmobi,(0.1,))

def testTD(threadnum): #Use thread.start_new_thread() to create 2 new threads
    for i in range(threadnum):
        thread.start_new_thread(mockTradingdesk,(0.1,))

def main():
    print './collector.py [td, ym] threadNum runHour'
    if sys.argv[1] == 'td':
        testTD(int(sys.argv[2]))
    elif sys.argv[1] == 'ym':
        testYM(int(sys.argv[2]))
    else:
        pass
    time.sleep(float(sys.argv[3])*3600)

if __name__=='__main__':
    main()