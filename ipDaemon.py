#!/usr/bin/env python

import sys, time
import logging
import urllib2
from DOApiService import DOApiService
from baseDaemon import Daemon



class MyDaemon(Daemon):

    LOG_FILENAME = '~/.ipdaemon/ip.log'
    CONF_FILENAME = '~/.ipdaemon/ipDaemon.cfg'
    MYIPSERVICE = 'http://myip.dnsdynamic.org/'
    ip = '0.0.0.0'
    def run(self):
        logging.basicConfig(filename=self.LOG_FILENAME, level=logging.DEBUG)
        while True:
            self.checkIp()
            service = DOApiService(self.ip, logging, self.CONF_FILENAME)
            service.runtrack(service.getrecords())
            time.sleep(1)


    def checkIp(self):
        try:
            ip = urllib2.urlopen(self.MYIPSERVICE).read()
            self.ip = ip
            message = "Retrieving Ip: %s" % ip
            self.debug(message)
        except Exception,e:
            self.debug('%s', e.message)


    def debug(self, string):
        return logging.debug(string)





if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[ 1 ]:
            daemon.start()
        elif 'stop' == sys.argv[ 1 ]:
            daemon.stop()
        elif 'restart' == sys.argv[ 1 ]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[ 0 ]
        sys.exit(2)