#! /usr/bin/env python

__author__ = 'jeff.yu'



with open('C:\Users\jeff.yu\Desktop\conv.ini', 'r') as f:
    lines = f.readlines()
print len(lines)
idList = []
for line in lines:
    line = line.strip()
    index = line.find('=')
    transaction_id = line[index+1:]
    idList.append(transaction_id)
print len(set(idList))

