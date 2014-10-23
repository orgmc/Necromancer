#! /usr/bin/env python
# --*-- coding:utf-8 --*--


from __future__ import division
import os
import sys

__author__ = 'jeff.yu'


def get_files(filemodle):
    log_path = sys.path[0] + '/log/'
    file_list = os.listdir('log')
    returnlist = []
    for file in file_list:
        if file.startswith(filemodle):
            returnlist.append(log_path + file)
    return returnlist

def get_first_time(file_list):
    process_time = {}
    for file in file_list:
        with open(file) as f:
            all_lines = f.readlines()
        for line in all_lines:
            strkey = line.split(' ')[0]
            try:
                floatkey = float(strkey)
            except ValueError as e:
                continue
            if process_time.has_key(floatkey):
                process_time[floatkey] = process_time[floatkey] + 1
            else:
                process_time[floatkey] = 1

    orderProcessTime = {}
    orderKeys = sorted(process_time.keys())
    sumCount = 0
    for orderKey in orderKeys:
        value = process_time.get(orderKey)
        orderProcessTime[orderKey] = value
        sumCount += value
    return process_time, sumCount

def get_process_time(file_list):
    process_time = {}
    for some_file in file_list:
        with open(some_file) as f:
            all_lines = f.readlines()
        for line in all_lines:
            key = get_processtime(line)
            if key == '':
                continue
            if process_time.has_key(key):
                process_time[key] = process_time[key] + 1
            else:
                process_time[key] = 1

    orderProcessTime = {}
    orderKeys = sorted(process_time.keys())
    sumCount = 0
    for orderKey in orderKeys:
        value = process_time.get(orderKey)
        orderProcessTime[orderKey] = value
        sumCount += value
    return process_time, sumCount

def writer(jsonData, sumCount, sheetName):
    """
    return: none
    write to excel file
    """
    try:
        import xlwt
    except ImportError as e:
        print """module xlwt not found, can't write data to excel file"""
        exit(-1)
    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet(sheetName)
    rows =  len(jsonData)
    # set worksheet table name
    worksheet.write(0, 0, "ProcessTime")
    worksheet.write(0, 1, "Count")
    worksheet.write(0, 2, "Percent")
    row = 1
    for key in jsonData:
        value = jsonData.get(key)
        worksheet.write(row, 0, key)
        worksheet.write(row, 1, value)
        percent = '{0}%'.format(str(round(value/sumCount, 4) * 100))
        worksheet.write(row, 2, percent)
        row += 1
        if row == rows + 1:
            break
    workbook.save("output/{0}.xls".format(sheetName))

def main():

    """
    NOTICE: 10-14 18:00:00:  as * 1682 processTime=193 appId=100 slotId=508 slotWidth=320 slotHeight=50 adNum=1 creativeId=0 adId=130 dspUserId=88888888 bid=0.2600000000 creativeType=1
    NOTICE: 10-14 18:00:00:  as * 1702 processTime=1 appId=100 slotId=508 slotWidth=320 slotHeight=50 adNum=1 creativeId=0 adId=130 dspUserId=88888888 bid=0.2600000000 creativeType=1
    grep -c "processTime=1"  会统计数processTime=1和以1开头的数字的所有行 即统计出2行
    grep -c -w "processTime=1"  则精确匹配单词"processTime=1"  即统计出1行
    return: None
    main function
    """
    as_file_list = get_files('as')
    bs_file_list = get_files('bs')
    ui_file_list = get_files('ui')
    host_file_list = get_files('host')

    as_data, asSumCount =  get_process_time(as_file_list)
    bs_data, bsSumCount =  get_process_time(bs_file_list)
    ui_data, uiSumCount=  get_process_time(ui_file_list)
    host_data, hostSumCount =  get_first_time(host_file_list)

    writer(as_data, asSumCount, "AsLogProcessTime")
    writer(bs_data, bsSumCount, "BsLogProcessTime")
    writer(ui_data, uiSumCount, "UiLogProcessTime")
    writer(host_data, hostSumCount, "HostLogProcessTime")

def get_processtime(line):
    start_index = line.find('processTime')
    if start_index == -1:
        return ''
    end_index = line.find('appId')
    return int(line[start_index:end_index].strip().split('=')[1])

if __name__ == '__main__':
    main()