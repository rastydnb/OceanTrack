#!/usr/bin/env python

from DOApiService import DOApiService
from ConfigParser import ConfigParser
import os
import errno


CONF_FILENAME = os.getenv("HOME")+'/.ipdaemon/ipDaemon.cfg'
apiservice = DOApiService(configfile=CONF_FILENAME)
configparser = ConfigParser()


# GET CREDENTIALS
cliendId = raw_input('Enter correct clientId to track the domain: ')
apiKey = raw_input('Enter correct apikey to track the domain: ')

apiservice.apiKey = apiKey
apiservice.apiDomain = 'https://api.digitalocean.com'
apiservice.getRecordUrl = '%s/domains/%s/records?client_id=%s&api_key=%s'
apiservice.getDomainsUrl = '%s/domains?client_id=%s&api_key=%s'
apiservice.clientId = cliendId
apiservice.apiKey = apiKey



domainsData = apiservice.getDomains()

for domain in domainsData['domains']:
    print 'id: %d => Domain: %s \n' % (domain['id'], domain['name'])

# DOMAIN TO CONFIG
print 'Which domain you want to track? \n'
domainId = raw_input('Enter correct id to track the domain: ')
apiservice.domainId = domainId

for domain in domainsData['domains']:
    if str(domain['id']) == domainId:
        domainData = domain

for record in apiservice.getrecords()['records']:
    print 'id: %d => Record: %s \n' % (record['id'], record['name'])

recordId = raw_input('Enter correct id to track the record: ')

timeout = raw_input('Enter update time in seconds: ')

def newconfig():

    configparser.add_section('CREDENTIALS')
    configparser.set('CREDENTIALS', 'ApiKey', apiKey)
    configparser.set('CREDENTIALS', 'CliendId', cliendId)

    configparser.add_section('DOMAIN')
    configparser.set('DOMAIN', 'Id', domainData['id'])
    configparser.set('DOMAIN', 'Name', domainData['name'])

    configparser.add_section('API-DATA')
    configparser.set('API-DATA', 'apiDomain', 'https://api.digitalocean.com')
    configparser.set('API-DATA', 'getRecordUrl', '%s/domains/%s/records?client_id=%s&api_key=%s')
    configparser.set('API-DATA', 'getDomainsUrl', '%s/domains?client_id=%s&api_key=%s')
    configparser.set('API-DATA', 'setRecordIpUrl', '%s/domains/%s/records/%s/edit?client_id=%s&api_key=%s&data=%s')
    configparser.set('API-DATA', 'recordId', recordId)

    configparser.add_section('UPDATE')
    configparser.set('UPDATE', 'timeout', timeout)


    dummy = open(CONF_FILENAME, 'w')
    configparser.write(dummy)
    dummy.close()

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
make_sure_path_exists(os.getenv("HOME")+'/.ipdaemon')
newconfig()

