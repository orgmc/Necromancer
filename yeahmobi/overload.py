#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

import os
from time import sleep
import re
pattern = r'"filter":"\S+druid.json"'

def modifyIndexFile(jsonfile, indexFile):
    with open(indexFile) as f:
        record = f.readline()
        newJsonFile = '"filter":"%s"' % indexFile
        record = re.sub(pattern, newJsonFile , record)
    with open(indexFile, 'w') as f:
        f.writelines(record)

def getJsonFile(parentdir):
    return os.listdir(parentdir)

def getIndexFile(parentdir):
    indexlist = os.listdir(parentdir)
    return [indexfile for indexfile in indexlist if indexfile.startswith('overlord.indexer.indexing.table')]


def importBatchJson(jsonfile, indexFile):

    modifyIndexFile(jsonfile, indexFile)
    command = """curl -i -L -X 'POST' -H 'Content-Type:application/json' -d @%s "http://localhost:8090/druid/indexer/v1/task" | awk '{print $0}'""" % (indexFile)
    print os.popen(command).read()

def main():

    batchJsonDir = raw_input("Enter basedir path: ")
    indexFileDir = raw_input("Enter indexfile path: ")
    jsonFileList, indexFileList = getJsonFile(batchJsonDir), getIndexFile(indexFileDir)
    print "get {0} json files:\n{1}".format(len(jsonFileList), jsonFileList)

    for jsonFile in jsonFileList:
        for indexFile in indexFileList:
            importBatchJson(jsonFile, indexFile)
            sleep(72000)

if __name__ == '__main__':
    main()