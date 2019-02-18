from bs4 import BeautifulSoup as bs
import json

def extract(infile,params):
	f = open(infile,'rU')
	t_dict = {}
	i = 0
	for line in f:
		if i == 0:
			pass
		else:
			contents = line.split('\t')
			ID = contents[params['Database identifier']].strip()
			eligible = contents[params['Eligible - Audit']]
			# print eligible
			if eligible == "1":
				# print 'yay'
				t_dict[ID] = {}
				for key,value in params.items():
					if key == 'Database identifier':
						continue
					else:
						t_dict[ID].update({key:contents[value]})
		i+=1
	f.close()

	return t_dict

wos_params = {
	'Name':12,
	'Title':4,
	'Publication':8,
	'Publication Year':7,
	# 'Address':None,
	# 'Document URL':None,
	'Database identifier':16,
	'Eligible - Audit':2,
	'Eligible - Race':0
}


### read in csv with studies that I tagged as eligible

wos_infile = 'C:/Users/Ole/Dropbox/@audits/searchresults/201408-eligible-studies-WOS.csv'
wos_dict = extract(wos_infile,wos_params)
# print wos_dict

### read in meta data of complete WOS search results file

infile = open('../temp/current-session.txt','rU')
temp_dict = json.load(infile)
infile.close()

 xml_file = temp_dict['XML file name']
# xml_file = "../temp/2014814-12384-searchresults-xml.txt"
time_stamp = temp_dict['Time stamp']
# time_stamp = "2014814-12384"

### read in complete WOS search results
xml_temp = open(xml_file,'rU')
xml_in = ""
for line in xml_temp:
	xml_in = xml_in + line
xml_in = '<top_level>'+xml_in+"</top_level>"
f = bs(xml_in,'xml')

### find address data

eligibles = wos_dict.keys()
primary_contact = {}
contact_dict = {}

n_found = 0
n_uid = 0
n_addr2 = 0

for record in f('REC'):	
	uid = str(record.UID.text).strip()
	n_uid += 1

	name = str()
	email = str()
	address = str()
	others = list()
	oname = list()
	oaddress = list()

	if uid in eligibles:
		n_found += 1
		for k in record.static_data.find_all('reprint_contact'):

			try:
				address = str(k.address_spec.full_address.text)
			except:
				address = "no address"
			
			try:
				name = str(k.full_name.text)
			except:
				name = "no name"
			try:
				email = str(k.email_addr.text)
			except:
				email = "no email"
				
		for j in record.static_data.fullrecord_metadata.find_all('addresses'):
			for m in j.find_all('address_name'):
				try:
					oaddress = str(m.full_address.text)
				except:
					oaddress = "no address"

				for p in m.find_all('name'):
					try:
						oname = str(p.full_name.text)
					except:
						oname = "no name"
					if oname == name:
						continue
					else:
						others.append([oname,oaddress])
					
		primary = [name,address,email]
		contact_dict[uid] = [primary,others]

	else:
		pass

print str(len(eligibles))+" eligible records"
print str(n_uid)+" UID records"
print str(n_found)+" matched records found"
print str(n_addr2)+" records with reprint info"

### write results to outcsv and outdoc
### csv: write one line per article author instead of one line per article
### txt: one entry per article

outcsv_name = '../results/%s-authorlist-new.csv' % (time_stamp)
outcsv = open(outcsv_name, 'w')
outcsv.write("WOS:ID"+"\t"+"Author - Last name"+"\t"+"Author - First name"+"\t"+"Publication year"+"\t"+"Title"+"\t"+"Publication title"+"\t"+"Author - Address"+"\t"+"Author - E-mail"+"\t"+"First author"+'\t'+"Focus on race (1) or other (0)"+"\n")

outdoc_name = '../results/%s-authorlist-new.txt' % (time_stamp)
outdoc = open(outdoc_name,'w')
outdoc.write('LIST OF AUDIT STUDY AUTHORS\n\n\n')

for key in wos_dict.keys():
	k = wos_dict[key]['Name'].split(',')
	last = k[0].strip()
	first = k[1].strip()
	ID = key
	pub = wos_dict[key]['Publication']
	pub_year = wos_dict[key]['Publication Year']
	title = wos_dict[key]['Title']
	racei = wos_dict[key]['Eligible - Race']
	outcsv.write(ID+'\t')
	outcsv.write(last+'\t')
	outcsv.write(first+'\t')
	outcsv.write(pub_year+'\t')
	outcsv.write(title+'\t')
	outcsv.write(pub+'\t')
	# outcsv.write(contact_dict[key][0][0]+"; ")
	outcsv.write(contact_dict[key][0][1]+"\t")
	outcsv.write(contact_dict[key][0][2]+"\t")
	outcsv.write("yes"+'\t')
	# for item in contact_dict[key][1]:
	#	outcsv.write(item[0])
	#	outcsv.write(' - ')
	#	outcsv.write(item[1])
	#	outcsv.write('; ')
	# outcsv.write('\t')
	outcsv.write(racei)
	outcsv.write('\n')

	for item in contact_dict[key][1]:
		j = item[0].split(',')
		jlast = j[0].strip()
		jfirst = j[1].strip()
		outcsv.write(ID+'\t')
		outcsv.write(jlast+'\t')
		outcsv.write(jfirst+'\t')
		outcsv.write(pub_year+'\t')
		outcsv.write(title+'\t')
		outcsv.write(pub+'\t')
		outcsv.write(item[1]+'\t\t')
		outcsv.write('no'+'\t')
		outcsv.write(racei)
		outcsv.write('\n')

	outdoc.write('First author: ')
	outdoc.write(contact_dict[key][0][0])
	outdoc.write('\n')
	outdoc.write('Address: ')
	outdoc.write(contact_dict[key][0][1])
	outdoc.write('\n')
	outdoc.write('email: ')
	outdoc.write(contact_dict[key][0][2])
	outdoc.write('\n')
	outdoc.write('Co-authors: ')
	for item in contact_dict[key][1]:
		outdoc.write(item[0])
		outdoc.write(' - ')
		outdoc.write(item[1])
		outdoc.write('; ')
	outdoc.write('\n')
	outdoc.write('Title: '+title)
	outdoc.write('\n')
	outdoc.write('Publication: '+pub)
	outdoc.write('\n')
	outdoc.write('Date: '+pub_year)
	outdoc.write('\n')
	outdoc.write('WOS ID: '+ID)
	outdoc.write('\n')
	outdoc.write('Date: '+pub_year)
	outdoc.write('\n')
	outdoc.write('Focus on race (1) or other (0): '+racei)
	outdoc.write('\n\n')

outcsv.close()
outdoc.close()