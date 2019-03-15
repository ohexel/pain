#!/usr/bin/env python
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
            'firstRecord' : start
        }

        return self.client['search'].service.search(qparams, rparams)

    def retrieve(self, queryid, start, count):
        self.queryId = str(queryid)
        rparams = { 
                'firstRecord' : int(start),
                'count' : int(count),
                'sortField' : [{
                    'name' : 'PY',
                    'sort' : 'D'
                    }]
                }
                
        return self.client['search'].service.retrieve(queryid, rparams)
        
def waiting(seconds):
    minutes=seconds//60
    print ("Wait %s minute(s)!" % minutes)
    waittime=seconds
    while waittime > 0:
        time.sleep(5)
        waittime-=5
        if waittime == 0:
            print("... let's go!")
        else:
            print("... %s seconds." % waittime)

# define a search query
journal = 'SO=(JOURNAL OF PAIN) OR SO=(PAIN)'
title = 'TI=(gender OR sex OR women)'
keywords01 = 'TS=(gender OR sex OR women)'
keywords02 = 'TS=((gender OR sex OR women) AND (opioid* OR opiate))'
keywords03 = 'TS=((opioid* OR opiate*) AND (addiction OR dependence OR misuse))'
query = str('(%s) AND (%s) AND (%s)' % (journal, title, keywords02))

# get first result and get number of records found to define number of loops
# since WoK web services only return 100 results at a time
soap = WokmwsSoapClient()
results = soap.search(query, 1, 0)
queryid = ''
for line in results:
    newline = str(line)
    newline = newline.strip(string.punctuation + string.whitespace)
    if 'recordsFound' in newline:
        word = newline
        word = word.translate(None, 'recordsFound')
        word = word.strip(string.punctuation + string.whitespace)
        all_the_records = int(word)
    if 'queryId' in newline:
        queryid = newline[-1]
print("There are %s records that match the query." % (all_the_records))


# make timestamp
year = time.localtime()[0]
month = time.localtime()[1]
day = time.localtime()[2]
hour = time.localtime()[3]
minute = time.localtime()[4]
second = time.localtime()[5]
time_stamp = '%s%s%s-%s%s%s' % (year,month,day,hour,minute,second)
searchresults_filename = './tmp/%s-search-results.txt' % (time_stamp)

# get ALL the records
# create output file for records and beautifulsoup object
first = 1
stack = 100
counter = 0
cycles = all_the_records / stack
stack_rest = all_the_records % stack
print ("Writing search results to %s." % (searchresults_filename))
outfile = open(searchresults_filename, 'w+')
record = str()
while counter <= cycles :
    if counter == cycles:
        stack = stack_rest
    print ("Attempt: %s. Retrieving %s records. QueryId: %s." % (counter+1, stack, queryid))
    results = soap.retrieve(queryid, start = first, count = stack)
    first = first + 100
    counter += 1
    for line in results:
        try:
            newline = str(line)
        except:
            newline = "Encoding error"
        outfile.write(newline)
        outfile.write('\n')
        record = record + newline + '\n'
outfile.close()
soap.close()

# dump session parameters to json for later retrieval
temp_dict = {'Search file name':searchresults_filename, 'Time stamp':time_stamp, 'Search query':query, 'Number of results':all_the_records}
if not os.access('./tmp/', os.W_OK):
    os.mkdir('./tmp/', 0o755)
session_file = './tmp/current-session.txt'
print("Writing session parameters to %s." % session_file)
if os.path.isfile(session_file):
    outfile = open(session_file,'w')
else:
    outfile = open(session_file,'w+')
json.dump(temp_dict,outfile)
outfile.close()
