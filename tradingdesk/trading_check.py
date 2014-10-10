#! /usr/bin/env python


import urllib2
from urllib import urlencode
from itertools import combinations
import json
from time import sleep, time
import logging


TRADING_JSON = '{"settings":{"process_type":"lp","report_id":"14029195015","return_format":"json","time":{"start":1404172800,"end":1409529600,"timezone":0},"data_source":"contrack_druid_datasource_ds","pagination":{"size":10,"page":0}},"data":["clicks","outs","ctr","convs","cr","cost","income","net","roi"],"filters":{"$and":{}},"sort":[],"group":%s}'
# COMMON_GROUP = ["device_id", "country_id","click_id","campaign_id","ref_site","site","click_time","cost_per_click","payout","real_ip","proxy_ip","os_id","carrier_id","mobile_brand_id","screen_h","screen_w","screen_id","city_id","brand_id","model_id","state_id","conversion_time","event","sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8"]
COMMON_GROUP = ["year", "month", "week", "day", "hour"]




class TradingCheck(object):
    def __init__(self):
        self.post_url = 'http://172.20.0.70:8080/trading/report?'


    def set_grouplist(self):
        self.tmplist = []
        for index in range(5):
            tmpgroup = list(combinations(COMMON_GROUP, index))
            for group in tmpgroup:
                self.tmplist.append(str(list(group)).replace("'", '"'))

    def check(self):
        self.set_grouplist()
        print 'generate group list success, totaly {0} records'.format(len(self.tmplist))
        for trading_json in self.tmplist:
            if trading_json == "[]":
                continue
            trading_json = trading_json.rstrip(']"') + '","offer_id"]'
            trading_data = TRADING_JSON % trading_json
            postdata = urlencode({'report_param': trading_data})
            try:
                rsp = urllib2.build_opener().open(urllib2.Request(self.post_url, postdata), timeout=50).read()
                rspdata = json.loads(rsp)['data']['data']
                if len(rspdata) <= 1:
                    print "error: " + trading_json
                else:
                    pass
            except Exception as e:
                print "unknow error: " + trading_json
            else:
                pass
        exit("execute test over")


if __name__ == '__main__':
    tc = TradingCheck()
    tc.check()


