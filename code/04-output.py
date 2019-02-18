import json
import os

infile = open('./tmp/current-session.txt','rU')
temp_dict = json.load(infile)
infile.close()

time_stamp = temp_dict['Time stamp']

### ALL DOCUMENTS

records_database = temp_dict['Records DB']

f = open(records_database,'rU')
recordsd = json.load(f)
f.close()

#   Output of records dictionary

onelevel_vars = ['Title','Abstract','Year Published','Date Published','Publication title','Volume','Issue']
twolevel_vars = ['Keywords','Primary author - full name','Primary author - WoS name','Authors - full names','Authors - Wos name']

csv_out = './results/%s-records.csv' % (time_stamp)

print "Writing results to %s." % (csv_out)

# write column headings
if not os.path.isdir('./results/'):
    os.mkdir('./results/')

if os.path.isfile(csv_out):
    outfile = open(csv_out,'w')
else:
    outfile = open(csv_out,'w+')
outfile.write('ID')
outfile.write('\t')
for var in onelevel_vars:
    outfile.write(var)
    outfile.write('\t')

for var in twolevel_vars:
    outfile.write(var)
    outfile.write('\t')

outfile.write("\n")

# write column contents

for id in recordsd.keys():
    outfile.write(id)
    outfile.write('\t')

    for var in onelevel_vars:
        outfile.write(str(recordsd[id][var]).strip())
        outfile.write('\t')
    
    for item in recordsd[id]['Keywords']:
        outfile.write(str(item).strip())
        outfile.write("; ")
    outfile.write('\t')

    # primary author, full name
    outfile.write(str(recordsd[id]['Authors'][0][0]).strip())
    outfile.write('\t')
    
    # primary author, wos name
    outfile.write(str(recordsd[id]['Authors'][0][1]).strip())
    outfile.write('\t')

    # all authors, full name
    for i in range(len(recordsd[id]['Authors'])):
        outfile.write(str(recordsd[id]['Authors'][i][0]))
        outfile.write("; ")
    outfile.write('\t')

    # all authors, wos name
    for i in range(len(recordsd[id]['Authors'])):
        outfile.write(str(recordsd[id]['Authors'][i][1]))
        outfile.write("; ")
    outfile.write('\t')

    outfile.write("\n")

outfile.close()

# OUTPUT session info

filename = './results/%s-session-info.txt' % (time_stamp)


print "Writing session info to %s." % (filename)

outfile = open(filename,'w')
for key,value in temp_dict.items():
    outfile.write(str(key)+': '+str(value)+'\n')
outfile.close()

"""
### ANNUAL STATS

f = open('../discr-annual-db.txt','rU')
atgb = json.load(f)
f.close()

#   Consistency checks

count = 0
single_count = 0
co_count = 0

for year in atgb:
    count = count + atgb[year]['count_articles']
    single_count = single_count + atgb[year]['count_single']
    co_count = co_count + atgb[year]['count_co']
    
# print count, single_count, co_count

#   Output of dictioary

outfile = open('../discr-years.csv','w')

#   first line
outfile.write('Year')
outfile.write('\t')
outfile.write('N - articles')
outfile.write('\t')
outfile.write('N - single-authored articles')
outfile.write('\t')
outfile.write('N - co-authored articles')
outfile.write('\t')
for i in range(10):
    varname1 = "Keyword " + str(i+1)
    varname2 = "Keyword odds ratio " + str(i+1)
    outfile.write(varname1)
    outfile.write('\t')
    outfile.write(varname2)
    outfile.write('\t')
for i in range(10):
    varname1 = "Abstract keyword " + str(i+1)
    varname2 = "AbKw odds ratio " + str(i+1)
    outfile.write(varname1)
    outfile.write('\t')
    outfile.write(varname2)
    outfile.write('\t')
outfile.write('\n')

#   data
for year in atgb:
    outfile.write(year)
    outfile.write('\t')
    outfile.write(str(atgb[year]['count_articles']))
    outfile.write('\t')
    outfile.write(str(atgb[year]['count_single']))
    outfile.write('\t')
    outfile.write(str(atgb[year]['count_co']))
    outfile.write('\t')
    
    if atgb[year]['Keyword frequencies']:
        end = 10
        if len(atgb[year]['Keyword frequencies']) < end:
            end = len(atgb[year]['Keyword frequencies'])
        for i in range(end):
            outfile.write(atgb[year]['Keyword frequencies'][i][1])
            outfile.write('\t')
            outfile.write(str(atgb[year]['Keyword frequencies'][i][0]))
            outfile.write('\t')
        end = 10
        if len(atgb[year]['Abstract Keyword frequencies']) < end:
            end = len(atgb[year]['Abstract Keyword frequencies'])
        for i in range(end):
            outfile.write(atgb[year]['Abstract Keyword frequencies'][i][1])
            outfile.write('\t')
            outfile.write(str(atgb[year]['Abstract Keyword frequencies'][i][0]))
            outfile.write('\t')
    outfile.write('\n')
outfile.close()
"""
