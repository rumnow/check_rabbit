#!/usr/bin/env python

import sys
import requests


def getargs(my_args):
    if '--help' in my_args:
        print 'Help for rabbit queue script:\n', \
            'Use this arguments for get length of queue:\n', \
            '--host \n--port \n--vhost \n--queue \n--user \n--password', \
            '\n--output simple or telegraf', \
            '\n    telegraf output like a DB, host, queue etc', \
            '\n --measurment for telegraf influxdb'
        sys.exit(1)
    know_args = {'--host': '', '--port': '', '--vhost': '',
                 '--queue': '', '--user': '', '--password': '',
                 '--output': 'simple', '--database': ''}
    for i in my_args:
        if i in know_args.keys():
            know_args[i] = my_args[my_args.index(i) + 1]
    return know_args


if __name__ == '__main__':
    # the one string below maybe delete
    test_arg = ['0', '--host', '172.33.1.1', '--port', '15672',
                '--vhost', 'qa_vi', '--queue', 'dev_todo',
                '--user', 'monitor', '--password', 'monitor_pass',
                '--output', 'telegraf', '--database', 'devrabbit']
    a = getargs(sys.argv)
    if len(sys.argv) < 17:
        print 'Too few params (need 8), try --help'
        sys.exit(1)

    url = 'http://' + a['--host'] + ':' + a['--port'] + '/api/queues/' + \
        a['--vhost'] + '/' + a['--queue']
    r = requests.get(url, auth=(a['--user'], a['--password']))

    if r.status_code == 200:
        if a['--output'] == 'simple':
            print r.json()['messages']
        elif a['--output'] == 'telegraf':
            print a['--database'] + ','+'host='+a['--host']+',' \
                  +'vhost=' + a['--vhost'] + ' ' + a['--queue'] \
                  + '='+str(r.json()['messages'])
        sys.exit(0)
    else:
        print 'Error ' + str(r.status_code)
        sys.exit(1)
