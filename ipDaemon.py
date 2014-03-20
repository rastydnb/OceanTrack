#!/usr/bin/env python

import sys, time
import logging
import urllib2
from DOApiService import DOApiService
from baseDaemon import Daemon
import os
from datetime import datetime as date
import gc



class MyDaemon(Daemon):

    LOG_FILENAME = os.getenv("HOME")+'/.ipdaemon/ip.log'
    CONF_FILENAME = os.getenv("HOME")+'/.ipdaemon/ipDaemon.cfg'
    MYIPSERVICE = 'http://myip.dnsdynamic.org/'
    ip = '0.0.0.0'
    def run(self):
        logging.basicConfig(filename=self.LOG_FILENAME, level=logging.DEBUG)
        while True:
            self.checkIp()
            service = DOApiService(self.ip, logging, self.CONF_FILENAME)
            service.runtrack(service.getrecords())
            time.sleep(int(service.updateTime))
            gc.collect()



    def checkIp(self):
        try:
            ip = urllib2.urlopen(self.MYIPSERVICE).read()
            self.ip = ip
            message = "Retrieving Ip: %s" % ip
            self.debug(message)
        except Exception,e:
            self.debug('%s', e.message)
        gc.collect()


    def debug(self, string):
        return logging.debug(string + ' date=>' + unicode(date.now()))






if __name__ == "__main__":
    daemon = MyDaemon('/tmp/OceanTrack.pid')
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
