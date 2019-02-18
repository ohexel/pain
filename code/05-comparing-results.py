# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 14:02:38 2014

@author: Walter
"""

import string

def strippin(somestring):
    s = str(somestring)
    s = s.strip()
    s = s.strip(string.whitespace)
    s = s.strip(string.punctuation)
    # s = s.remove(string.punctuation[1])
    # s = s.remove(string.punctuation[6])
    s = s.lower()
    return s

newresults = open("C:/Users/Ole/Dropbox/@audits/webofknowledge/results/2014926-153245-records.csv", "rU")
newdict = {}

skipfirstline = True

for line in newresults:
    if skipfirstline == True:
        skipfirstline = False
        continue
    else:
        contents = line.split('\t')
        """
        # the following was necessary to render current WOS id's comparable
        # to previous ID formats
        k = contents[0].split(':')
        identifier = k[1]
        test = True
        while test == True:
            if identifier[0] == "0":
                identifier = identifier[1:]
            else:
                test = False
        """
        identifier = strippin(contents[0])
        title = strippin(contents[1])
        abstract = strippin(contents[2])
        author = strippin(contents[9])
        year = strippin(contents[3])
        publication = strippin(contents[5])
        newdict[identifier] = {'Author':author,'Title':title,'Abstract':abstract,'Publication':publication,'Year':year}
newresults.close()

oldresults = open("C:/Users/Ole/Dropbox/@audits/webofknowledge/results/2014814-12384-records.csv","rU")
olddict = {}

skipfirstline = True

for line in oldresults:
    if skipfirstline == True:
        skipfirstline = False
        continue
    else:
        contents = line.split('\t')
        identifier = strippin(contents[0])
        title = strippin(contents[1])
        abstract = strippin(contents[2])
        author = strippin(contents[9])
        year = strippin(contents[3])
        publication = strippin(contents[5])
        olddict[identifier] = {'Author':author,'Title':title,'Abstract':abstract,'Publication':publication,'Year':year}
oldresults.close()

outfile = open("../results/201409-newnewresults.csv","w")

i = 0
j = 0

for key,value in newdict.items():
    if key not in olddict.keys():
        i += 1
        outfile.write(key+'\t')
        outfile.write(value['Author']+'\t')
        outfile.write(value['Title']+'\t')
        outfile.write(value['Abstract']+'\t')
        outfile.write(value['Publication']+'\t')
        outfile.write(value['Year']+'\n')
outfile.close()

outfile = open("../results/201409-newoldresults.csv","w")

for key,value in olddict.items():
    if key not in newdict.keys():
        j += 1
        outfile.write(key+'\t')
        outfile.write(value['Author']+'\t')
        outfile.write(value['Title']+'\t')
        outfile.write(value['Abstract']+'\t')
        outfile.write(value['Publication']+'\t')
        outfile.write(value['Year']+'\n')
outfile.close()
    
print "Number of old records that are not among new records: "+str(j)
print "Number of new records that are not among old records: "+str(i)