#! /usr/bin/env python

__author__ = 'jeff.yu'

import urllib
import urllib2
import json


def get_query(queryType, queryData):

    """
    :param queryType: ("yeahmobi", "tradingdesk")
    :param queryData: dimensions from spec file
    :return:
    """
    if queryType == 'tradingdesk':
        queryTemplate = '{"settings":{"time":{"start":1413288000,"end":1413288600,"timezone":0},"return_format":"json", "report_id":"232sds3232","data_source":"contrack_druid_datasource_ds","pagination":{"size":10000000,"page":0}},"group":["%s"],"data":["clicks","outs","ctr"],"filters":{"$and":{}},"sort":[]}'
    elif queryType == 'yeahmobi':
        queryTemplate = '{"settings":{"time":{"start":1413288000,"end":1413288600,"timezone":0},"data_source":"ymds_druid_datasource","report_id":"report-id","pagination":{"size":10000000,"page":0}},"group":["%s"],"data":["click","conversion"],"filters":{"$and":{}},"sort":[]}'
    else:
        print("invalid queryType")
        exit(-1)
    return queryTemplate % queryData


def get_httpdata(queryUrl, query):
    para_data = {"report_param":  query}
    post_data = urllib.urlencode(para_data)
    try:
        f = urllib2.build_opener().open(urllib2.Request(queryUrl, post_data), timeout=120)
    except Exception as e:
        raise  e
    try:
        content = f.read()
        jsonData = json.loads(content)
        return jsonData['data']['page']['total']
    except Exception as e:
        raise  e


def get_count(queryType, query):

    if queryType == 'tradingdesk':
        queryUrl = 'http://resin-track-1705388256.us-east-1.elb.amazonaws.com:18080/report/report?'
    elif queryType == 'yeahmobi':
        queryUrl = 'http://resin-yeahmobi-214401877.us-east-1.elb.amazonaws.com:18080/report/report?'
    else:
        pass
    count = get_httpdata(queryUrl, query)
    return count

def reverseData(jsonData):

    reverseJsonData = {}
    keys = jsonData.keys()
    for key in keys:
        value = jsonData.get(key)
        reverseJsonData[value] = key
    return reverseJsonData

def echoToStdout(jsonData):

    keys = jsonData.keys()
    sortedKeys = sorted(keys)
    for sortedKey in sortedKeys:
        value = jsonData.get(sortedKey)
        print value, sortedKey


def main():

    yeahmobiDimensions = ["transaction_id","visitor_id", "aff_id","aff_manager","aff_sub1","aff_sub2","aff_sub3","aff_sub4","aff_sub5","aff_sub6","aff_sub7","aff_sub8","adv_id","adv_manager","adv_sub1","adv_sub2","adv_sub3","adv_sub4","adv_sub5","adv_sub6","adv_sub7","adv_sub8","offer_id","rpa","cpa","ref_track","ref_track_site","ref_conv_track","click_ip","conv_ip","click_time","conv_time","time_diff","user_agent","browser","device_brand","device_model","device_os","device_type","country","time_stamp","log_tye","x_forwarded_for","state","city","isp","mobile_brand","platform_id","screen_width","screen_height","type_id","conversions","track_type","session_id","visitor_node_id","expiration_date","is_unique_click","gcid","gcname","browser_name","device_brand_name","device_model_name","platform_name","device_type_name","os_ver_name","os_ver"]
    tradingdeskDimensions = ["time_stamp","click_id","campaign_id","offer_id","ref_site","site","click_time","real_ip","proxy_ip","device_id","os_id","carrier_id","mobile_brand_id","cost_per_click","payout","screen_h","screen_w","screen_id","city_id","brand_id","model_id","country_id","state_id","conversion_time","event","sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8","sub_campaign_id"]

    yeahmobi = {}
    for dimension in yeahmobiDimensions:
        query = get_query('yeahmobi', dimension)
        yeahmobi[dimension] = get_count('yeahmobi', query)
    print yeahmobi
    # echoToStdout(reverseData(yeahmobi))
    print '---' * 20
    tradingdesk = {}
    for dimension in tradingdeskDimensions:
        query = get_query('tradingdesk', dimension)
        tradingdesk[dimension] = get_count('tradingdesk', query)
    print tradingdesk
    # echoToStdout(reverseData(tradingdesk))



if __name__ == '__main__':
    main()