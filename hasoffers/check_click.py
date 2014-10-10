#! /usr/bin/env python

__author__ = 'jeff.yu'

import json


def get_log_count(log_path):

    fobj = open(log_path, 'r')
    for line in fobj:
        for data in line:
            print data

if __name__ == '__main__':
    get_log_count('test.log')
