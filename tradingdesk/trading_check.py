#! /usr/bin/env python


import urllib2
from urllib import urlencode
from itertools import combinations
import json
from time import sleep, time
import logging


TRADING_JSON = '{"settings":{"process_type":"lp","report_id":"14029195015","return_format":"json","time":{"start":1325376000,"end":1451606400,"timezone":0},"data_source":"contrack_druid_datasource_ds","pagination":{"size":10,"page":0}},"data":["clicks","outs","ctr","convs","cr","cost","income","net","roi"],"filters":{"$and":{}},"sort":[],"group":%s}'
COMMON_GROUP = ["device_id", "os_id", "carrier_id", "country_id","ref_site","site","mobile_brand_id","screen_h","screen_w","city_id","brand_id","model_id","state_id","sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8","year","month","day","week","hour"]
#dont forget payout

import logging

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='tradingdesk.log',
        filemode='w')


class TradingCheck(object):
    def __init__(self):
        self.post_url = 'http://172.20.0.70:8080/track/report?'

    def set_grouplist(self):
        self.tmplist = []
        for index in range(5):
            tmpgroup = list(combinations(COMMON_GROUP, index))
            for group in tmpgroup:
                self.tmplist.append(str(list(group)).replace("'", '"'))
    def check(self):
        self.set_grouplist()
        count = 1
        maxcount = len(self.tmplist)
        print 'generate group list success...... {0} records'.format(maxcount)

        for trading_json in self.tmplist:
            if trading_json == "[]":
                continue
            trading_json = trading_json.rstrip(']"') + '","offer_id"]'
            trading_data = TRADING_JSON % trading_json
            postdata = urlencode({'report_param': trading_data})
            try:
                rsp = urllib2.build_opener().open(urllib2.Request(self.post_url, postdata), timeout=30).read()
                rspdata = json.loads(rsp)['data']['data']
            except Exception as e:
                logging.debug('failed: {0}'.format(trading_data))
            print "run {0} of {1}".format(count, maxcount)
            count += 1
            sleep(10)
        exit("exit when error")


if __name__ == '__main__':
    tc = TradingCheck()
    tc.check()


