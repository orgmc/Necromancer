#! /usr/bin/env python


import os
import time
from random import randint

ISOTIMEFORMAT = '%Y-%m-%d %X'


class TradingDesk(object):

    def __init__(self):
        self.data = {
        "time_stamp": "",
        "click_id": "43306130-ff65-436b-9851-1e265bc63ee1",
        "campaign_id": '55568',
        "offer_id": -1,
        "ref_site": "",
        "site": "",
        "click_time": "",
        "cost_per_click": 10.264,
        "payout":4.491,
        "real_ip": "147.12.35.1",
        "proxy_ip": "172.30.14.11",
        "device_id": 2,
        "os_id": 5,
        "carrier_id": 1,
        "mobile_brand_id": 3,
        "screen_h": 6,
        "screen_w": 8,
        "screen_id": 7,
        "city_id": 2,
        "brand_id": 1,
        "model_id": 4,
        "country_id": 3,
        "state_id": 4,
        "conversion_time": "",
        "event": 1,
        "sub1": "",
        "sub2": 4234,
        "sub3": "",
        "sub4": "",
        "sub5": "",
        "sub6": "",
        "sub7": "",
        "sub8": "",
        "click": 1,
        "lp_click": 0,
        "conversion": 0
    }
        self.kafka = '172.20.0.51:9092'
        self.topic_name = 'py_trading_desk'
        self.click_ids = ["43306130-ff65-436b-9851-1e265bc63ee1",
                         "43306131-ff65-436b-9851-1e265bc63ee1",
                         "43306132-ff65-436b-9851-1e265bc63ee1",
                         "43306133-ff65-436b-9851-1e265bc63ee1",
                         "43306134-ff65-436b-9851-1e265bc63ee1",
                         "43306135-ff65-436b-9851-1e265bc63ee1"]
        self.campaign_ids = ["12", "13", "15", "9", "22", "99"]
        self.offer_ids = [-1, 102, 902, 89, 77, 22, 33]
        self.ref_sites = ["www.baidu.com", "www.google.com", "www.yahoo.com",
                          "www.oracle.com", "www.yeahmobi.com", "www.csdn.com"]
        self.sites = ["baidu", "alibaba", "google", "yahoo", "csdn", "yeahmobi"]
        self.real_ips = ["17.12.5.10", "47.12.3.1", "17.1.35.1", "47.12.35.1", "147.13.35.1", "147.12.35.2" ]
        self.proxy_ips = ["12.10.14.11", "17.30.1.11", "172.20.15.12", "79.2.14.11", "129.3.124.11", "1.3.14.11"]
        self.common_ids = [1, 2, 3, 4, 5, 6]
        self.screen_hs = [10, 20, 30, 40, 50, 60]
        self.screen_w = [30, 50, 70, 90, 110, 130]


    def set_data(self):
        timenow = time.strftime(ISOTIMEFORMAT, time.localtime()).split()
        self.data['time_stamp'] = timenow[0] + 'T' + timenow[1] + 'Z'
        self.data['click_id'] = self.click_ids[randint(0, 5)]
        self.data['campaign_ids'] = self.click_ids[randint(0, 5)]
        self.data['offer_id'] = self.offer_ids[randint(0, 5)]
        self.data['ref_site'] = self.ref_sites[randint(0, 5)]
        self.data['site'] = self.sites[randint(0, 5)]
        self.data['real_ip']= self.real_ips[randint(0, 5)]
        self.data['proxy_ip'] = self.proxy_ips[randint(0, 5)]
        self.data['device_id'] = self.common_ids[randint(0, 5)]
        self.data['os_id'] = self.common_ids[randint(0, 5)]
        self.data['carrier_id'] = self.common_ids[randint(0, 5)]
        self.data['mobile_brand_id'] = self.common_ids[randint(0, 5)]
        self.data['screen_h'] = self.common_ids[randint(0, 5)]
        self.data['screen_w'] = self.common_ids[randint(0, 5)]
        self.data['screen_id'] = self.common_ids[randint(0, 5)]
        self.data['city_id'] = self.common_ids[randint(0, 5)]
        self.data['brand_id'] = self.common_ids[randint(0, 5)]
        self.data['model_id'] = self.common_ids[randint(0, 5)]
        self.data['country_id'] = self.common_ids[randint(0, 5)]
        self.data['state_id'] = self.common_ids[randint(0, 5)]
        self.data['event'] = self.common_ids[randint(0, 5)]
        self.data['sub1'] = self.common_ids[randint(0, 5)]
        self.data['sub2'] = self.common_ids[randint(0, 5)]
        self.data['sub3'] = self.common_ids[randint(0, 5)]
        self.data['sub4'] = self.common_ids[randint(0, 5)]
        self.data['sub5'] = self.common_ids[randint(0, 5)]
        self.data['sub6'] = self.common_ids[randint(0, 5)]
        self.data['sub7'] = self.common_ids[randint(0, 5)]
        self.data['sub8'] = self.common_ids[randint(0, 5)]
        self.data['lp_click'] = [0, 1][randint(0, 1)]
        if self.data['conversion'] == 1:
            self.data['click'] == 1
            self.data['click_time'] = timenow[0] + 'T' + timenow[1] + 'Z'
            self.data['conversion_time'] = timenow[0] + 'T' + timenow[1] + 'Z'


    def pass_data(self):
        self.set_data()
        cmd = 'java -jar prouder.jar {0} {1} {2}'.format(self.kafka, self.topic_name, self.data)
        print cmd
        cmd_rsp = os.popen(cmd).read()


if __name__ == '__main__':
    td = TradingDesk()
    for i in range(10):
        td.pass_data()