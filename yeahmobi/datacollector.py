#! /usr/bin/env python

import time
import thread
import os
import re


count = 0


def click(no, sleeptime):
    global  count
    while True:
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", count
        click_rsp = os.popen(""" curl 'http://172.30.10.146:8080/trace?offer_id=13580&aff_id=90010408&aff_sub=affsub&aff_sub2=affsub2&aff_sub3=affsub3&aff_sub4=affsub4&aff_sub5=affsub5&aff_sub6=affsub6&aff_sub7=affsub7&aff_sub8=affsub8' -A "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5" -i -l --header "referer:http://www.65536_click_1913.com" -H x-forwarded-for:54.86.55.142 """).read()
        time.sleep(sleeptime)
        click_id = get_id(click_rsp)
        conv_rsp = os.popen(""" curl 'http://172.30.10.146:8080/conv?transaction_id={0}' -i -l --header "referer:http://www.65536_conv_1914.com" -H x-forwarded-for:54.86.55.142 """.format(click_id)).read()
        count += 1
    thread.exit_thread()

def countdown(maxcount):
    click_count = 0
    conv_count = 0

    for i in range(maxcount):
        print click_count, '\t', conv_count
        click_rsp = os.popen(""" curl 'http://172.30.10.146:8080/trace?offer_id=13580&aff_id=90010408&aff_sub=affsub&aff_sub2=affsub2&aff_sub3=affsub3&aff_sub4=affsub4&aff_sub5=affsub5&aff_sub6=affsub6&aff_sub7=affsub7&aff_sub8=affsub8' -A "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5" -i -l --header "referer:http://www.65536_click_1913.com" -H x-forwarded-for:54.86.55.142 """).read()
        if click_rsp:
            click_count += 1
            click_id = get_id(click_rsp)
            if click_id:
                conv_count += 1
                conv_rsp = os.popen(""" curl 'http://172.30.10.146:8080/conv?transaction_id={0}' -i -l --header "referer:http://www.65536_conv_1914.com" -H x-forwarded-for:54.86.55.142 """.format(click_id)).read()

def get_id(click_rsp):
    for line in click_rsp.split('\n'):
        if line.startswith('Location'):
            line = line.strip()
            start_index = line.find('track=')
            end_index = line.find('&affiliateid=90010408')
            clickid = line[start_index+6:end_index]
            return clickid

def test(): # Use thread.start_new_thread() to create 2 new threads
    for i in range(10):
        thread.start_new_thread(click,(i+1, 0.1))


if __name__=='__main__':
    # collector_data()
    # test()
    # time.sleep(6*3600)
    countdown(1000)

