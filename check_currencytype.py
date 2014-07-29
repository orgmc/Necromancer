#! /usr/bin/env python

import urllib2
import urllib
import json
import sys
from decimal import Decimal



DIFF_CURRENCY_TYPE = [u'USD', u'GBP', u'EUR', u'HKD', u'CNY','MYR','ZAR','CHF']
CURRENCY_TYPE_POST = '{"settings":{"report_id":"1402919015","return_format":"json","time":{"start":%d,"end":%d,"timezone":0},"data_source":"ymds_druid_datasource","pagination":{"size":10000,"page":0}},"filters":{"$and":{"currency":{"$eq":"%s"}}},"data":["cost","revenue","profit"],"group":%s,"currency_type":"%s"}'
NO_CURRENCY_TYPE_POST = '{"settings":{"report_id":"1402919015","return_format":"json","time":{"start":%d,"end":%d,"timezone":0},"data_source":"ymds_druid_datasource","pagination":{"size":10000,"page":0}},"filters":{"$and":{"currency":{"$eq":"%s"}}},"data":["cost","revenue","profit"],"group":%s}'
URL='http://172.20.0.69:8080/realquery/report?'



def currency_convert(start, end, groupitem, topnitem=None): # group by adv_id and offer_id
    success = 0
    failed = 0
    for from_currency in DIFF_CURRENCY_TYPE:
        for to_currency in DIFF_CURRENCY_TYPE:
            if from_currency == to_currency:
                continue
            rate_from_to, rate_usd_to  = get_rate(from_currency, to_currency)
            real_result = get_data(start, end, from_currency, groupitem, None, to_currency)
            expect_result = get_data(start, end, from_currency, groupitem)

            for result in expect_result:
                result['cost'] = hround(result['cost'] * rate_usd_to, 3)
                result['revenue'] = hround(result['revenue'] * rate_from_to, 3)
                result['profit'] = str(round(Decimal(result['revenue']) - Decimal(result['cost']), 3))

            for result in real_result:
                result['cost'] = str(format(result['cost']))
                result['revenue'] = str(format(result['revenue']))
                result['profit'] = str(format(result['profit']))
            print real_result
            print expect_result
            if real_result == expect_result:
                success += 1
            else:
                failed += 1
    if failed == 0:
        return 'pass'
    return 'failed'

def get_data(start, end, from_currency, groupitem, topnitem=None, to_currency=None):
    if not to_currency:
        postdata = NO_CURRENCY_TYPE_POST % (start, end, from_currency, groupitem)
    else:
        postdata = CURRENCY_TYPE_POST % (start, end, from_currency, groupitem, to_currency)
    if topnitem:
        postdata = postdata.rstrip('}') + ',"topn":{0}'.format(topnitem) + '}'
    dataset = json.loads(urllib2.build_opener().open(urllib2.Request(URL, urllib.urlencode({'report_param': postdata}))).read())['data']['data']
    key, values = dataset[0], dataset[1:]
    datalst = []
    for value in values:
        datalst.append(dict(zip(key, value)))
    return datalst

def get_rate(from_currency, to_currency):
    for rate in CURRENCY_TABLE:
        if rate.get('currency_from') == from_currency and rate.get('currency_to') == to_currency:
            return (rate.get('rate_from_to'), rate.get('rate_usd_to'))

def get_currency():
    get_url = 'http://172.20.0.51:9099/xchangeRates?params%3D%7B%22query_type%22%3A%22all%22%2C%22return_format%22%3A%22json%22%2C%22query_id%22%3A%2288e771bc-a11-44dd-afa2-9fcc056e9eeb%22%2C%22colums%22%3A%5B%22currency_from%22%2C%22currency_to%22%2C%22rate_from_to%22%2C%22rate_usd_to%22%5D%7D'
    return json.loads(urllib2.urlopen(urllib2.Request(get_url)).read()).get('rates')


def hround(num, prc=3):
    strnum = repr(num)
    strnum_len = len(strnum)
    p_dot = strnum.find('.')

    if strnum_len - 1 - p_dot < prc+1:
        return strnum

    strnum_list = list(strnum[:p_dot+prc+2])

    keynum = int(strnum_list[p_dot+prc+1])
    if keynum >= 5:
        tmp = int(strnum_list[p_dot+prc])
        if tmp + 1 == 10:
            strnum_list[p_dot+prc] = '0'
            if int(strnum_list[p_dot+prc-1]) + 1 == 10:
                strnum_list[p_dot+prc-1] = '0'
                if int(strnum_list[p_dot+prc-2]) + 1 == 10:
                    strnum_list[p_dot+prc-2] = '0'
                    strnum_list[p_dot+prc-4] = str(int(strnum_list[p_dot+prc-4]) + 1)
                else:
                    strnum_list[p_dot+prc-2] = str(int(strnum_list[p_dot+prc-2]) + 1)
            else:
                strnum_list[p_dot+prc-1] = str(int(strnum_list[p_dot+prc-1]) + 1)
        else:
            strnum_list[p_dot+prc] = str(tmp + 1)


    tmpstrnum = str(float(''.join(strnum_list[:p_dot+prc+1])))
    return tmpstrnum



if __name__ == '__main__':
    CURRENCY_TABLE = get_currency()
    print currency_convert(1400112000, 1405728000, '["aff_manager", "aff_id", "offer_id", "currency"]', '{"metricvalue":"cost","threshold":3}')
    # print test_aff_off(1400112000, 1405728000)
    # print test_am_aff_off_topn(1400112000, 1405728000)
    # print test_am(1400112000, 1405728000)
    # print test_adv_off(1400112000, 1405728000)