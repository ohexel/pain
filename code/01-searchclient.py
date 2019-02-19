#!/usr/bin/env python2
"""
Web of Knowledge search client
2019/01
Ole Hexel

Based on the WokmwsSoapClient written by Dominik Moritz
https://gist.github.com/domoritz/2012629
"""

from suds.client import Client
from suds.transport.http import HttpTransport
import urllib2
import string
import time
import json
import os
#import logging

class HTTPSudsPreprocessor(urllib2.BaseHandler):
    def __init__(self, SID):
        self.SID = SID

    def http_request(self, req):
        req.add_header('cookie', 'SID="'+self.SID+'"')
        return req

    https_request = http_request


class WokmwsSoapClient():
    """
    main steps you have to do:
        soap = WokmwsSoapClient()
        results = soap.search(...)
    """
    def __init__(self):
        self.url = self.client = {}
        self.SID = ''

        self.url['auth'] = 'http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl'
        self.url['search'] = 'http://search.webofknowledge.com/esti/wokmws/ws/WokSearch?wsdl'

        self.prepare()

    def __del__(self):
        self.close()

    def prepare(self):
        """does all the initialization we need for a request"""
        self.initAuthClient()
        self.authenticate()
        self.initSearchClient()

    def initAuthClient(self):
        self.client['auth'] = Client(self.url['auth'])

    def initSearchClient(self):
        http = HttpTransport()
        opener = urllib2.build_opener(HTTPSudsPreprocessor(self.SID))
        http.urlopener = opener
        self.client['search'] = Client(self.url['search'], transport = http)

    def authenticate(self):
        self.SID = self.client['auth'].service.authenticate()

    def close(self):
        self.client['auth'].service.closeSession()

    """
    def search(self, query, start, stack):
        qparams = {
            'databaseId' : 'WOS',
            'userQuery' : query,
            'queryLanguage' : 'en',
            'editions' : [{
                'collection' : 'WOS',
                'edition' : 'SSCI',
            }]
        }

        rparams = {
            'count' : stack, # 1-100
            'firstRecord' : start,
            #'fields' : [{
            #    'name' : 'Relevance',
            #    'sort' : 'D'
            #}]
        }
    """

    def search(self, query, start, stack):
        qparams = {
            'databaseId' : 'WOS',
            'userQuery' : query,
            'queryLanguage' : 'en',
            'editions' : [{
                'collection' : 'WOS',
                'edition' : 'SCI',
            },{
                'collection' : 'WOS',
                'edition' : 'SSCI',
            }]
        }

        rparams = {
            'count' : stack, # 1-100
            'firstRecord' : start,
            'fields' : [{
                'name' : 'Relevance',
                'sort' : 'D'
            }]
        }

        return self.client['search'].service.search(qparams, rparams)
        
soap = WokmwsSoapClient()

# turn on logging for debugging
"""
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.INFO)
logging.getLogger('suds.xsd.schema').setLevel(logging.WARNING)
logging.getLogger('suds.wsdl').setLevel(logging.INFO)
logging.getLogger('suds.resolver').setLevel(logging.WARNING)
logging.getLogger('suds.xsd.query').setLevel(logging.INFO)
logging.getLogger('suds.xsd.basic').setLevel(logging.WARNING)
logging.getLogger('suds.binding.marshaller').setLevel(logging.WARNING)
"""

# define a search query
query = 'TS=(opiod)  and TS=(gender) and TS=(women)'

# get first result and get number of records found to define number of loops
# since WoK web services only return 100 results at a time

results = soap.search(query, 1, 1)
time.sleep(1)   # necessary to avoid WoK block

for line in results:
    newline = str(line)
    newline = newline.strip(string.punctuation + string.whitespace)
    if 'recordsFound' in newline:
        word = newline
        word = word.translate(None, 'recordsFound')
        word = word.strip(string.punctuation + string.whitespace)
        all_the_records = int(word)

print str(all_the_records)+" records matching the query have beend found."

# get ALL the records
# create output file for records and beautifulsoup object

first = 1
stack = 100
count = 0
cycles = all_the_records / stack
stack_rest = all_the_records % stack

year = time.localtime()[0]
month = time.localtime()[1]
day = time.localtime()[2]
hour = time.localtime()[3]
minute = time.localtime()[4]
second = time.localtime()[5]

time_stamp = '%s%s%s-%s%s%s' % (year,month,day,hour,minute,second)
searchresults_filename = './tmp/%s-search-results.txt' % (time_stamp)

temp_dict = {'Search file name':searchresults_filename, 'Time stamp':time_stamp, 'Search query':query, 'Number of results':all_the_records}

# dump search results filename to json for later retrieval
if not os.access('./tmp/', os.W_OK):
    os.mkdir('./tmp/', 0755)
session_file = './tmp/current-session.txt'
if os.path.isfile(session_file):
    outfile = open(session_file,'w')
else:
    outfile = open(session_file,'w+')
json.dump(temp_dict,outfile)
outfile.close()

print "Search results are being written to "+searchresults_filename

outfile = open(searchresults_filename, 'w+')
record = str()

while count <= cycles :
    if count == cycles:
        stack == stack_rest
    results = soap.search(query, first, stack)
    first = first + 100
    count += 1

    for line in results:
        try:
            newline = str(line)
        except:
            newline = "Encoding error"
        # newline = newline.strip(string.punctuation + string.whitespace)
        outfile.write(newline)
        outfile.write('\n')
        record = record + newline + '\n'
    
    time.sleep(1)
    
outfile.close()
soap.close()
