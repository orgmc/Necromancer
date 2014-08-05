#! /usr/bin/env python


import re
import os
import time
from functools import wraps

_IP_PATTERN = re.compile(r'ip parser cost:\d+\s*ms')
_UA_PATTERN = re.compile(r'ua parser cost:\d+\s*ms')
_JUMP_PATTERN = re.compile(r'save JumpLog cost:\d+\s*ms')


def timediff(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print '>> Spend {1} seconds'.format(func.__name__, end - start)
        return result
    return wrapper


class LogParser(object):
    def __init__(self, filepath, ip_count =0 , ua_count =0, jump_count =0,
                 ip_cost_file =None, ua_cost_file =None, jump_cost_file =None):

        self._file = filepath
        self._ip_cost_file = ip_cost_file
        self._ua_cost_file = ua_cost_file
        self._jump_cost_file = jump_cost_file
        self._ip_total = ip_count
        self._ua_total = ua_count
        self._jumps_total = jump_count
        self._ips = {}
        self._uas = {}
        self._jumps = {}
        self.parser()
        self.sort_cost()

    @timediff
    def parser(self):

        with open(self._file, 'r') as f:
            if self._ip_cost_file:
                for line in f:
                    ip_cost = line.strip().split(':')[-1]
                    if ip_cost not in self._ips:
                        self._ips[ip_cost] = 1
                    else:
                        self._ips[ip_cost] += 1
            if self._ua_cost_file:
                for line in f:
                    ua_cost = line.strip().split(':')[-1]
                    if ua_cost not in self._uas:
                        self._uas[ua_cost] = 1
                    else:
                        self._uas[ua_cost] += 1
            if self._jump_cost_file:
                for line in f:
                    jump_cost = line.strip().split(':')[-1]
                    if jump_cost not in self._jumps:
                        self._jumps[jump_cost] = 1
                    else:
                        self._jumps[jump_cost] += 1

    def sort_cost(self):
        if self._ips:
            fobj = open(self._ip_cost_file, 'w')
            keys = self._ips.keys()
            sort_keys = sorted(keys, key = lambda x:int(x.strip('ms')))
            for skey in sort_keys:
                single_costs = self._ips[skey]
                cost_percent = '{0}%'.format(round(single_costs / float(self._ip_total), 4) * 100)
                fobj.writelines('{0}\t\t{1}\t\t{2}\n'.format(skey, single_costs, cost_percent))
            fobj.close()

        if self._uas:
            fobj = open(self._ua_cost_file, 'w')
            keys = self._uas.keys()
            sort_keys = sorted(keys, key = lambda x:int(x.strip('ms')))
            for skey in sort_keys:
                single_costs = self._uas[skey]
                cost_percent = '{0}%'.format(round(single_costs / float(self._ua_total), 4) * 100)
                fobj.writelines('{0}\t\t{1}\t\t{2}\n'.format(skey, single_costs, cost_percent))
            fobj.close()

        if self._jumps:
            fobj = open(self._jump_cost_file, 'w')
            keys = self._jumps.keys()
            sort_keys = sorted(keys, key = lambda x:int(x.strip('ms')))
            for skey in sort_keys:
                single_costs = self._jumps[skey]
                cost_percent = '{0}%'.format(round(single_costs / float(self._jumps_total), 4) * 100)
                fobj.writelines('{0}\t\t\t{1}\t\t\t{2}\n'.format(skey, single_costs, cost_percent))
            fobj.close()

@timediff
def split_logfile(filepath):
    ip_log = open('ip_tmplog', 'w')
    ua_log = open('ua_tmplog', 'w')
    jump_log = open('jump_tmplog', 'w')

    ip_count = ua_count = jump_count = 0


    with open(filepath) as f:
        for line in f:
            search_ip = _IP_PATTERN.search(line)
            if search_ip:
                ip_count += 1
                ip_log.writelines(search_ip.group() + '\n')
            search_ua = _UA_PATTERN.search(line)
            if search_ua:
                ua_count += 1
                ua_log.writelines(search_ua.group() + '\n')
            search_jump = _JUMP_PATTERN.search(line)
            if search_jump:
                jump_count += 1
                jump_log.writelines(search_jump.group() + '\n')

    ip_log.close()
    ua_log.close()
    jump_log.close()

    return (ip_count, ua_count, jump_count)

def cleanup():
    try:
        os.remove('ip_tmplog')
        os.remove('ua_tmplog')
        os.remove('jump_tmplog')
    except Exception as e:
        pass

def get_input():
    entry_logpath = 'Enter log file name: '
    entry_ip_cost_file = 'Enter ip cost file name you wanna create: '
    entry_ua_cost_file = 'Enter ua cost file name you wanna create: '
    entry_jump_cost_file = 'Enter jump cost file name you wanna create: '
    logpath = raw_input(entry_logpath)
    print
    ip_cost_file = raw_input(entry_ip_cost_file)
    print
    ua_cost_file = raw_input(entry_ua_cost_file)
    print
    jump_cost_file = raw_input(entry_jump_cost_file)
    print
    if os.path.exists(logpath):
        pass
    else:
        exit('Sorry, log file does not exist, exit now!')

    if os.path.exists(ip_cost_file):
        exit('Sorry, "{0}" is already exist, exit now!'.format(ip_cost_file))

    if os.path.exists(ua_cost_file):
        exit('Sorry, "{0}" is already exist, exit now!'.format(ua_cost_file))

    if os.path.exists(jump_cost_file):
        exit('Sorry, "{0}" is already exist, exit now!'.format(jump_cost_file))


    return logpath, ip_cost_file, ua_cost_file, jump_cost_file

def main():
    log_path, ip_cost_file, ua_cost_file, jump_cost_file = get_input()
    print 'Start split log file...... '
    ip_total, ua_total, jump_total = split_logfile(log_path)
    print '>> Split log file success\n\nStart analyse ip cost...... '
    lp = LogParser('ip_tmplog', ip_count= ip_total, ip_cost_file= ip_cost_file)
    print '>> Analyse ip cost success\n\nStart analyse ua cost ...... '
    lp = LogParser('ua_tmplog', ua_count= ua_total, ua_cost_file= ua_cost_file)
    print '>> Analyse ua cost success\n\nStart analyse save jump cost...... '
    lp = LogParser('jump_tmplog', jump_count= jump_total, jump_cost_file= jump_cost_file)
    print '>> Analyse save jump cost success\n\nRun script over\n'
    cleanup()


if __name__ == '__main__':
    main()