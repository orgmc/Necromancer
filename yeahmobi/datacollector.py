# coding:utf-8


"""

construct some special data for yeahmobi referer and session ip alarm regression testing

step 1: change local machine time zone to utc

step 2: make sure field in excel file is correct


"""


import xlrd
import urllib
import json
import time
import random


ISOTIMEFORMAT='%Y-%m-%d %X'

class DataCollector(object):

    def __init__(self, filepath):
        self.excelpath = filepath

    def get_excel_data(self, log_type):

        fobj = xlrd.open_workbook(self.excelpath)
        if not fobj:
            exit('no file found, check it again')
        table = fobj.sheets()[0]
        rows = table.nrows
        keys = [str(data) for data in table.row_values(0) if data != '']
        values = []
        for row in range(rows):
            if row == 0:
                continue
            temp = table.row_values(row)
            value = []
            for v in temp:
                try:
                    v = str(int(v))
                except Exception:
                    pass
                if v != '':
                    value.append(v)
            values.append(value)
        self.maps = []
        for value in values:
            data = dict(zip(keys, value))
            data['device_model'] = ''
            if log_type == 0:
                data['click_time'] = time.strftime(ISOTIMEFORMAT, time.localtime())
                data['conv_ip'] = ''
                data['log_type'] = '0'
            elif log_type == 1:
                data['click_time'] = time.strftime(ISOTIMEFORMAT, time.localtime())
                time.sleep(random.randint(0, 5))
                data['conv_time'] = time.strftime(ISOTIMEFORMAT, time.localtime())
                data['log_type'] = '1'
            self.maps.append(data)


    def data_sync(self):

        # click data
        self.get_excel_data(0)
        for data in self.maps:
            json_duble_str = json.dumps(data).replace("'", '"')
            url = 'http://172.20.0.69:8080/collector/collector?collector_param={0}&platformName=yfnormalpf'.format(data)
            print urllib.urlopen(url).getcode()

        # conv data
        self.get_excel_data(1)
        for data in self.maps:
            json_duble_str = json.dumps(data).replace("'", '"')
            url = 'http://172.20.0.69:8080/collector/collector?collector_param={0}&platformName=yfnormalpf'.format(data)
            print urllib.urlopen(url).getcode()


if __name__ == '__main__':
    dc = DataCollector(r'F:\work\session ip alarm.xlsx')
    dc.data_sync()
