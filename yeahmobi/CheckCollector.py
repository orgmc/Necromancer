#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'


import sys
import json
from collections import Counter



def checkDuplicate(recordFile, recordType):

    with open(recordFile) as f:
        lines = f.readlines()

    if recordType == 'batch':
        jsonLines = (json.loads(line) for line in lines)
        all_transactions = (line.get('transaction_id') for line in jsonLines)
        all_logtypes = (line.get('log_type') for line in jsonLines)
    else:
        splitLines = (line.split('\001') for line in lines)
        all_transactions = (line[28] for line in splitLines)
        all_logtypes = (line[37] for line in splitLines)

    transaction_count = Counter(all_transactions)
    repeatTransactionId = []

    for transaction in transaction_count:
        if transaction_count.get(transaction) > 2:
            repeatTransactionId.append(transaction)

    clicks = 0
    conversions = 0

    for log_type in all_logtypes:
        if log_type == '0':
            clicks += 1
        elif log_type == '1':
            conversions += 1
        else:
            pass

    display = "File: [{0}]:\n\t{1} records \n\t{2} clicks \n\t{3} conversions\n\t duplicate transaction_id:{4}".format(
        recordFile, clicks, conversions, repeatTransactionId
    )

    print display

if __name__ == '__main__':
    recordFile = sys.argv[1]
    recordType = sys.argv[2]
    if recordType not in ('hadoop', 'batch'):
        print 'recordType should be hadoop or batch'
        exit(-1)
    checkDuplicate(recordFile)