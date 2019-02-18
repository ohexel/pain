from bs4 import BeautifulSoup as bs
import string
import json

def format_string(some_string):
    # Quotation marks are interpreted as text delimiters in .csv files; whenever
    # they occur in strings, they are replaced with two grave accents
    
    inchar = string.punctuation[1]+string.punctuation[6]
    outchar = string.punctuation[27]+string.punctuation[27]
    transtable = string.maketrans(inchar, outchar)

    return (str(some_string).strip()).translate(transtable,"\n\t")
        
def process_record(rec):
    uid = str(rec.UID.text)    # WoS-specific record ID
    #   print uid            # useful to find the record where script breaks
    
    ### AUTHORS
    # find all authors of a publication and put them in a list

    authors = []
    
    for name in rec.names.find_all('name'):
        full_name = str(name.full_name.text)
        wos_name = str(name.wos_standard.text)
        rank = str(name["seq_no"])
        name_info = [full_name, wos_name, rank]
        authors.append(name_info)
    
    # add the authors and the publication ID to the author dictionary
    
    for person in authors:
        if person[1] not in authorsd.keys():
            authorsd[person[1]] = {'Publications': [], 'Keywords' : []}
        if uid not in authorsd[person[1]]['Publications']:
                authorsd[person[1]]['Publications'].append(uid) 
    
    ### KEYWORDS
    # find all keywords, put them in a list
    
    keywords = []
    try:
        if not rec.keywords:
            for word in rec.keywords_plus('keyword'):
                kword = format_string(word.text).title()
                keywords.append(kword)
        else:
            for word in rec.keywords('keyword'):
                kword = format_string(word.text).title()
                keywords.append(kword)
    except:
        pass
    
    # add keywords to author dictionary
    # no check for duplicates or similar spellings

    for person in authors:
        authorsd[person[1]]['Keywords'].append(keywords)

    # BIBLIOGRAPHIC INFO
    
    for item in rec.titles('title'):
        if item['type'] == "item":
            doc_title = format_string(item.text).title()
        elif item['type'] == "source":
            pub_title = format_string(item.text).title()
        else:
            continue
    
    try:
         pub_volume = str(rec.pub_info['vol'])
    except:
        pub_volume = ""
    
    try:
        pub_issue = str(rec.pub_info['issue'])
    except:
        pub_issue = ""

    pub_year = str(rec.pub_info['pubyear'])
    pub_date = str(rec.pub_info['sortdate'])
    
    # ABSTRACT
    
    if rec.pub_info['has_abstract'] == "Y":
        if int(rec.abstracts['count']) > 1:
            doc_abstract = str()
            print uid+" has more than one abstract"
        else:
            doc_abstract = format_string(rec.abstract_text.text)
    else:
        doc_abstract = str()

    # add everything to records dictionary

    recordsd[uid] = { 'Title': doc_title,
                     'Authors': authors,
                     'Keywords': keywords,
                     'Abstract': doc_abstract,
                     'Year Published': pub_year, 
                     'Date Published': pub_date,
                     'Publication title': pub_title,
                     'Volume': pub_volume,
                     'Issue': pub_issue
                     }
    
    """
    # within records dictionary, create a "author position" key with value "author name"

    for person in authors:
        key_name = "author_"+str(authors.index(person)+1)
        recordsd[uid][key_name] = person
    """
    
print "This is happening."

# BeautifulSoup needs one and only one top-level tag
# the Soap response and extraction method result in several concatenatd, 
# same-level <records> tags. Therefore, I drop these and add a top-level
# <allrecords> tag.

infile = open('./tmp/current-session.txt','rU')
temp_dict = json.load(infile)
infile.close()

searchresults_xml = temp_dict['XML file name']
time_stamp = temp_dict['Time stamp']

infile = open(searchresults_xml, 'rU')
fullrecords = ""
for line in infile:
    if ('<records' in line) or ('</records>' in line) or (line.isspace()):
        continue
    else:
        fullrecords = fullrecords + line
infile.close()

fullrecords = fullrecords.strip()

fullrecords = "<allrecords>" + "\n" + fullrecords + "</allrecords>"

### MAKE SOUP
print "Making the soup."
soup = bs(fullrecords, 'xml')

# dump soup to json

out_filename = './tmp/%s-searchresults-soupified.txt' % (time_stamp)
temp_dict['Soup file name'] = out_filename

outfile = open(out_filename,"w")
temp = fullrecords[12:-13]
#print temp[-5:]
json.dump(temp,outfile)
outfile.close()


### EAT SOUP

recordsd = dict()
authorsd = dict()

print "Begin processing."

for record in soup('REC'):
    process_record(record)

print "Processing done."

### OUTPUT
#   dump to json to do other stuff w/o reading in big files

records_database = './tmp/%s-records-database.txt' % (time_stamp)
author_database = './tmp/%s-author_database.txt' % (time_stamp)
temp_dict['Records DB'] = records_database
temp_dict['Author DB'] = author_database

print "Dumping databases to %s and %s." % (records_database,author_database)

f = open(records_database,'w')
json.dump(recordsd,f)
f.close()

f = open(author_database,'w')
json.dump(authorsd,f)
f.close()

outfile = open('./tmp/current-session.txt','w')
json.dump(temp_dict,outfile)
outfile.close()

#   Consistency checks
#   TO DO
