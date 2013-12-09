#!/usr/bin/env python

import json
import urllib2
import logging
from ConfigParser import ConfigParser
import pprint
import sys

class DOApiService:

    ip = ''
    clientId = ''
    apiKey = ''
    domainId = ''
    log = None
    apiDomain = ''
    getRecordUrl = ''
    setRecordIpUrl = ''
    getDomainsUrl = ''
    configfile = ''
    recordId = ''
    updateTime = ''


    def __init__(self, ip='0.0.0.0', logging=None, configfile=None):
        self.ip = ip
        self.log = logging
        self.configfile = configfile
        try:
            self.readconfig()
        except Exception, e:
            return




    def getrecords(self):
        response = urllib2.urlopen(self.getRecordUrl % (self.apiDomain, self.domainId, self.clientId, self.apiKey))
        records = json.loads(response.read())
        return records




    def setrecordip(self, id):
        logging.debug(id)
        urllib2.urlopen(self.setRecordIpUrl % (self.apiDomain, self.domainId, id, self.clientId, self.apiKey, self.ip))
        logging.debug('Ip changed')

    def getDomains(self):
        response = urllib2.urlopen(self.getDomainsUrl % (self.apiDomain, self.clientId, self.apiKey))
        domains = json.loads(response.read())
        return domains

    def runtrack(self, records):
        for record in records['records']:
            if str(record['id']) == str(self.recordId):
                logging.debug(record['name'])
                logging.debug(record['data'])
                if record['data'] != self.ip:
                    self.setrecordip(record['id'])

    def readconfig(self):
        configparser = ConfigParser()
        configparser.read(self.configfile)

        self.apiDomain = configparser.get('API-DATA', 'apiDomain')
        self.getRecordUrl = configparser.get('API-DATA', 'getRecordUrl')
        self.getDomainsUrl = configparser.get('API-DATA', 'getDomainsUrl')
        self.setRecordIpUrl = configparser.get('API-DATA', 'setRecordIpUrl')
        self.recordId = configparser.get('API-DATA', 'recordId')

        self.apiKey = configparser.get('CREDENTIALS', 'ApiKey')
        self.clientId = configparser.get('CREDENTIALS', 'CliendId')

        self.domainId = configparser.get('DOMAIN', 'Id')

        self.updateTime = configparser.get('UPDATE', 'timeout')



