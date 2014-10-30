#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

import pymongo
import os
from time import sleep
import urllib2
import urllib
import json
import redis
from random import choice


def get_data(query_data):

    query_url = "http://172.20.0.69:8080/realquery/report?"
    para_data = {"report_param":  query_data}
    post_data = urllib.urlencode(para_data)
    try:
        f = urllib2.build_opener().open(urllib2.Request(query_url, post_data), timeout = 60).read()
        format_data = json.loads(f)['data']['data']
        if len(format_data) > 1:
            return format_data
        else:
            return None
    except Exception as e:
        return None
    return format_data

def getOffInfo():

    # connect redis on 172.30.10.147
    r = redis.Redis(host='172.30.10.147', port=6378, db=0)
    offerList = ["7704", "90010531", "90010607", "5986"]
    affList = ["11021", "90010420", "90010587"]
    return offerList, affList

class CheckConversion(object):

    def __init__(self):
        self._setConnection()
        self._getTransactionid()

    def _setConnection(self):
        conn = pymongo.Connection('172.30.10.147',27017)
        self.clickLogHasoffer = conn.report.click_log

    def _getTransactionid(self):
        dataSet = self.clickLogHasoffer.find()
        self.transactionidList = []
        for data in dataSet:
            self.transactionidList.append(data.get(u'_id'))

    def _updateRecord(self, transaction_id):
        offerList, affList = getOffInfo()
        self.clickLogHasoffer.update({'_id':transaction_id}, {'$set':{'offer':choice(offerList)}})
        self.clickLogHasoffer.update({'_id':transaction_id}, {'$set':{'aff':choice(affList)}})


    def _sendConv(self):
        sumCount = len(self.transactionidList)
        print 'get {0} transaction_id'.format(sumCount)
        for transaction_id in self.transactionidList:
            print transaction_id
            self._updateRecord(transaction_id)
            curlCommand = """curl 'http://172.30.10.146:8080/conv?transaction_id={0}&adv_sub=advsub&adv_sub2=advsub2&adv_sub3=advsub3&adv_sub4=advsub4&adv_sub5=advsub5&adv_sub6=advsub6&adv_sub7=advsub7&adv_sub8=advsub8' -i -l --header "referer:http://www.65536_conv_1914.com" -H x-forwarded-for:54.86.55.142""".format(transaction_id)
            print curlCommand
            # print os.popen(curlCommand).read()
            # sleep(10)
            # if self._isFound(transaction_id):
            #     print 'pass........'
            # else:
            #     print 'failed......'

    def _isFound(self, transaction_id):
        queryStr = '{"settings":{"time":{"start":1414022400,"end":1414108800,"timezone":0},"data_source":"ymds_druid_datasource","report_id":"report-id","pagination":{"size":50,"page":0}},"group":[],"data":["click","conversion"],"filters":{"$and":{"transaction_id":{"$eq":"%s"}}},"sort":[]}' % transaction_id
        if get_data(queryStr):
            return True
        return False



if __name__ == '__main__':

    cc = CheckConversion()
    cc._sendConv()