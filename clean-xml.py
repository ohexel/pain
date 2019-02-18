#!/usr/bin/env python3
from bs4 import BeautifulSoup as bs
import string
import json

infile = open("examples/xml-example", 'rU')
fullrecords = ""
for line in infile:
    if ('<records' in line) or ('</records>' in line) or (line.isspace()):
        continue
    else:
        fullrecords = fullrecords + line
infile.close()
fullrecords = fullrecords.strip()
fullrecords = "<allrecords>" + fullrecords + "</allrecords>"
soup = bs(fullrecords, 'xml')
nresults = fullrecords.count('/REC')
print "N results:" + str(nresults)
print "Names: " + str(soup.names.find('display_name').text)
