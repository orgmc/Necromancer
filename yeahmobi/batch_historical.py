#! /usr/bin/env python

import time
import thread
import os
import urllib2
import urllib
import time

count = 0

def click(sleeptime):
    ISOTIMEFORMAT='%Y-%m-%d %X'
    global count
    while True:
	print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', count
	data = {'collector_param':{"aff_id":"65536","aff_manager":"8","aff_sub1":"affsub","aff_sub2":"affsub2","aff_sub3":"affsub3","aff_sub4":"affsub4","aff_sub5":"affsub5","aff_sub6":"affsub6","aff_sub7":"affsub7","aff_sub8":"affsub8","adv_id":"624","adv_manager":"0","adv_sub1":"affsub","adv_sub2":"advsub2","adv_sub3":"advsub3","adv_sub4":"advsub4","adv_sub5":"advsub5","adv_sub6":"advsub6","adv_sub7":"advsub7","adv_sub8":"advsub8","offer_id":"65536","currency":"GBP","rpa":"20.0","cpa":"15.0","click_ip":"54.86.55.142","conv_ip":"54.86.55.142","transaction_id":"f899c145-a5da-4998-b683-44d21df10752","click_time": time.strftime(ISOTIMEFORMAT, time.localtime()),"conv_time":time.strftime(ISOTIMEFORMAT, time.localtime()),"user_agent":"Mozilla/5.0+(iPhone;+U;+CPU+iPhone+OS+4_3_2+like+Mac+OS+X;+zh-cn)+AppleWebKit/533.17.9+(KHTML+like+Gecko)+Version/5.0.2+Mobile/8H7+Safari/6533.18.5","browser":"1","device_model":"1","os_ver":"0","country":"ZZ","log_type":"1","visitor_id":"3274c4c8-0f0c-4517-8956-77eef6a21d83","forward_ips":"127.0.0.1","state":"-1","city":"-1","isp":"-1","mobile_brand":"-1","platform_id":"1","screen_width":"320","screen_height":"480","conversions":"","track_type":"0","session_id":"e97f1f87-7a08-4b0a-8465-02bf53c5685f","visitor_node_id":"ubuntu-template","expiration_date":"2014-12-05","is_unique_click":"1","gcid":"","gcname":"","browser_name":"Mobile+Safari","device_brand_name":"Apple","device_brand":"1","device_model_name":"iPhone","device_type_name":"Mobile","device_type":"1","platform_name":"iOS","os_ver_name":"4.3.2","ref_conv_track":"http://www.65536_conv_07081624.com","referer":"http://www.65536_click_1913.com"},'platformName':'yfnormalpf'}
	postdata = urllib.urlencode(data)
        rsp = urllib2.build_opener().open(urllib2.Request('http://172.20.0.69:8080/collector/collector?', postdata)).read()
        time.sleep(sleeptime)
	count += 1
    thread.exit_thread()

def test(): #Use thread.start_new_thread() to create 2 new threads
    for i in range(20):
        thread.start_new_thread(click,(0.1,))


if __name__=='__main__':
    test()
    time.sleep(24*3600)