#! /usr/bin/env python

#!/usr/bin/env python

# -*- coding: utf-8 -*-



import pexpect
import ConfigParser


def druidup():
    choice = raw_input('start or stop all druid node, include <broker, realtime and historical> \n'
                       'stop or start: ')
    conf = ConfigParser.ConfigParser()
    conf.read('machinelist/machinelist.ini')
    brokerlist = conf.get('broker', 'ip').split(',')
    realtimelist = conf.get('realtime', 'ip').split(',')
    historicallist = conf.get('historical', 'ip').split(',')

    if choice == 'start':
        print 'start broker ......'
        for ip in brokerlist:
            ssh_cmd(ip, '111111', '/dianyi/druid-services-0.6.52/broker.startup.sh')
            print 'start broker: {0} success'.format(ip)

        print 'start realtime ......'
        for ip in realtimelist:
            ssh_cmd(ip, '111111', '/dianyi/druid-services-0.6.52/realtime.startup.sh')
            print 'start realtime: {0} success'.format(ip)

        print 'start historical ......'
        for ip in historicallist:
            ssh_cmd(ip, '111111', '/dianyi/druid-services-historical/historical.startup.sh')
            print 'start historical: {0} success'.format(ip)

    elif choice == 'stop':

        print 'stop broker ......'
        for ip in brokerlist:
            ssh_cmd(ip, '111111', 'pkill -9 broker')
            print 'stop broker: {0} success'.format(ip)

        print 'stop realtime ......'
        for ip in realtimelist:
            ssh_cmd(ip, '111111', 'pkill -9 realtime')
            print 'stop realtime: {0} success'.format(ip)

        print 'stop historical ......'
        for ip in historicallist:
            ssh_cmd(ip, '111111', 'pkill -9 historical')
            print 'stop historical: {0} success'.format(ip)

    else:
        print 'entery start or stop!'


def ssh_cmd(ip, passwd, cmd):
    ret = -1
    ssh = pexpect.spawn('ssh ubuntu@%s "%s"' % (ip, cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
        if i == 0 :
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
        ssh.sendline(cmd)
        r = ssh.read()
        print r
        ret = 0
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
    return ret


if __name__ == '__main__':
    druidup()
