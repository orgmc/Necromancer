#! /usr/bin/env python
# coding=utf-8


import urllib2
from urllib import urlencode
from itertools import combinations
from datetime import  datetime
import time

"""
    用户比较常用的组织方式如下：
 Country  = all
(Country = * ) and  (Carrier = all) ,
(Country = * ) and  (Device = all) ,
(Country = * ) and  (OS = all) ,
(Country = * ) and  (Sub1 = all) ,
(Country = * ) and  (Sub2 = all) ,
(Country = * ) and  (Sub3 = all) ,
(Country = * ) and  (Sub4 = all) ,
(Country = * ) and  (Sub1 = *)  and (Sub2=*) and (Sub3=*) and (Sub4=*),

Brand = all
Brand = *

Sub1 = All
Sub2 = All
Sub3 = All
Sub4 = All
(Sub1 = *)  and  (Sub2=*)  and （其它组合条件）

Hour = All

注：
1、以上的条件按照日常使用的优先次序排列，上面的优先级更高
2、所有的条件都同时包含Campaign=*  , 时区 = * ，时间段= * 到 *
3、* 代表某个具体的值

"""

DIMENSION = ("device_id", "carrier_id", "brand_id", "country_id", "os_id", "sub1", "sub2", "sub3", "sub4")
FILTER_DIMENSION = ("device_id", "carrier_id", "brand_id", "country_id", "os_id", "sub1", "sub2", "sub3")
GET_URL = '{"settings":{"time":{"start":1404182561,"end":1404889680,"timezone":0},"data_source":"contrack_druid_datasource_ds","pagination":{"size":1000000,"page":0}},"group":%s,"data":["clicks","outs","ctr","cr","income","cost","convs","cr","roi","net"],"filters":{"$and":{"campaign_id":{"$eq":"p_262"},%s}},"sort":[]}'
DIMENSIONMAP = {"country_id":{"$eq":4573}, "device_id":{"$eq":41}, "brand_id":{"$eq":848}, "os_id":{"$eq":261}, "carrier_id":{"$eq":2407034},"sub1":{"$eq":"005452f8-0147-1000-cd91-3f7332870066"},"sub2":{"$eq":"1386506376383030"},"sub3":{"$eq":1}}

def set_get_url():

    # get dimension combinations
    dimensionlst = []
    for i in range(len(DIMENSION)):
        for d in combinations(DIMENSION, i+1):
            dimensionlst.append(str(list(d)).replace("'", '"'))

    # get filter dimension
    filterlst = []
    for i in range(len(FILTER_DIMENSION)):
        for fitler_dimension in combinations(FILTER_DIMENSION, i+1):
            tmp = {}
            for d in fitler_dimension:
                tmp[d] = DIMENSIONMAP.get(d)
        tmp = '{0}'.format(tmp)
        tmp = tmp.replace("'", '"')
        filterlst.append(tmp.lstrip('{').rstrip('}') + '}')


    get_url_lst = []

    for dimension in dimensionlst:
        for filter_item in filterlst:
            get_url_lst.append(GET_URL % (dimension, filter_item))
    return get_url_lst


def get_dimension_data():

    run_lst = []
    POST_URL = 'http://resin-track-1705388256.us-east-1.elb.amazonaws.com:18080/report/report?'
    url_lst = set_get_url()
    print 'totaly {0} urls'.format(len(url_lst))
    index = 1
    for data in url_lst:
        postdata = urlencode({'report_param': data})
        begin = datetime.now()
        rsp = urllib2.build_opener().open(urllib2.Request(POST_URL, postdata)).read()
        end = datetime.now()
        time_diff = (end - begin).microseconds
        run_lst.append((time_diff, data))
        print '{0}, {1}, {2}'.format(index, time_diff, data)
        index += 1
        #time.sleep(0.5)

    fobj = open('result', 'w')
    sort_run_lst = sorted(run_lst, key=lambda x:x[0])
    for result in sort_run_lst:
        fobj.writelines(result + '\n')
    fobj.close()



if __name__ == '__main__':
    get_dimension_data()
