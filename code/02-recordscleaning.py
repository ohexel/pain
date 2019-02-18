"""
Soap responses have xml inside parentheses, i.e. responses look like this: 
(queryID=""),(records <>...<>). This script extracts xml delineated by 
<records> ... </records>. There is a comprehensive and a targeted way to
 extract records. The first function extracts the full xml information
from the soap response. The second function extracts only those xml records that correspond to a certain
document typ (articles, editorial, book review, ...). 
"""

from bs4 import BeautifulSoup as bs 
import json

# This extracts the entire <records>...</records> section inside each query response
def extract_full_records(filename):			
	data_in  = open(filename, 'rU')
	bulk = str()
	for line in data_in:
		bulk = bulk + line
	data_in.close()
     
	# print len(bulk)

	bulk_xml = str()
	xml_count = bulk.count('queryId')		# find out how many queries are in the file (= nbr of <records>...</records> pieces)
	
	print xml_count
	print filename

	for i in range(xml_count):
		start_record = bulk.index('<records')
		end_record = bulk.index('</records>')
		bulk_xml = bulk_xml + bulk[start_record:(end_record+len('</records>'))] + '\n'	# add <record> section to xml object
		new_bulk = bulk.partition('</records>')		# chop up bulk into processed section, delimiter and rest
		bulk = new_bulk[2]							# define rest as 'bulk' for further processing

	return bulk_xml


# This extracts only a certain type of record (inside <REC> ... </REC>), indicated by <doctype code="">
# from inside the entire <records>...</records> section. Here, I extract only articles.
# WOS doc_type codes: L - Letter, E - Editorial Material, R - Review, B - Book Review (R / B overlap unclear), 
# D - Discussion, P - Proceedings Paper, I - Item about an Individual, C - Correction, @ - Article

def extract_articles(filename):			# soap response has xml inside of tuples; extract xml delineated by <records> ... </records>
	data_in  = open(filename, 'rU')
	bulk = str()
	for line in data_in:
		bulk = bulk + line
	data_in.close()

	xml_count = bulk.count('queryID')		# find out how many queries are in the file (= nbr of <records>...</records> pieces)
	articles_xml = str()

	for i in range(xml_count):
		start_record = bulk.index('<records>')
		end_record = bulk.index('</records>')
		query_section = bulk[start_record:(end_record+len('</records>'))] 
		new_bulk = bulk.partition('</records>')		# chop up bulk into processed section, delimiter and rest
		bulk = new_bulk[2]						# define rest as 'bulk' for further processing

		pho = bs(query_section, 'xml')
		for rec in pho('REC'):
			if rec.doctype['code'] != '@':		# if document type not 'article', discard
				continue
			else:
				articles_xml = articles_xml + str(rec) + '\n'

	return articles_xml


infile = open('./tmp/current-session.txt', 'rU')
temp_dict = json.load(infile)
infile.close()

searchresults_filename = temp_dict['Search file name']
searchresults_timestamp = temp_dict['Time stamp']

print "Begin xml-ification."

xmlfile = extract_full_records(searchresults_filename)

out_filename = './tmp/%s-searchresults-xml.txt' % (searchresults_timestamp)

print "Writing xml to %s." % (out_filename)

data_out = open(out_filename, 'w')
for line in xmlfile:
	data_out.write(line)
data_out.close()

# dump temp file names to json for later retrieval
temp_dict['XML file name'] = out_filename

outfile = open('./tmp/current-session.txt','w')
json.dump(temp_dict,outfile)
outfile.close()
