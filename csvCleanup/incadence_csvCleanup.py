#!/usr/bin/python
import time
import csv
import re
import locations
from locations import parser
import clearances
from clearances import clearance as clear
from sys import argv
import companyinfo
from companyinfo import infofiller
import cleanTags
from cleanTags import cleanTag
import datetime
import categories
from categories import category
#  clearance,description,title,reqid,loclink,location,clearanceAndJunk
#csvFile = 'csvWork.csv'
logFile = 'logfile'
csvFile = 'csvWork.csv'
outFile = 'csvFinal.csv'
clearance = ""
doneThis = {}

tssci  = 'TS/SCI'
tssci2 = 'TS//SCI'
sec    = 'SECRET'
sec2   = 'Secret'
ts     = 'Top Secret'
dhs    = 'DHS'
LOG = open(logFile, 'w')

logDate= datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
companyName = 'Incadence'


# Open CSV output stream
output = open('/home/jbaker/Desktop/'+companyName+'_'+logDate+'_'+outFile, 'wb')
wr = csv.writer(output, quoting=csv.QUOTE_ALL)

csv.register_dialect(
  'mydialect',
  delimiter=',',
  quotechar='"',
  doublequote=True,
  skipinitialspace=True,
  lineterminator='\r\n',
  quoting=csv.QUOTE_MINIMAL)

wr.writerow(['title', 'apply_url', 'job_description', 'location', 'company_name', 'company_description', 'company_website', 'company_logo', 'company_facebook', 'company_twitter', 'company_linkedin', 'career_id', 'deployment', 'travel', 'job_lat', 'job_lon', 'company_benefits', 'job_category', 'clearance', 'keywords','author'])

infoComp,infoDesc,infoSite,infoLogo,infoFace,infoTwit,infoLinked,infoBeni,author=companyinfo.infofiller(companyName)

with open(csvFile, 'rb') as mycsv:
  data=csv.reader(mycsv, dialect='mydialect')
  for row in data:
    clearL,keyL,keyw = '','',''
    title  = row[0]
    desc   = row[1]
    req    = row[2]
    desc   = row[3]
    loc    = row[4]
    loc    = re.sub("<.+>(.+)<.+>",r'\1',loc)
    title  = re.sub("<.+>(.+)<.+>",r'\1',title)
    appUrl = req
    job_category = category(title)
    if re.match('Other', job_category):
      job_category = category(desc)
    if re.match('location', loc):
      LOG.write("Skipping header field")
    elif re.match('^$', loc):
      LOG.write("Empty location")
    elif len(desc) == 0:
      LOG.write("This one has an empty desc.")
    elif doneThis.has_key(req):
      LOG.write("Already done this crap...")
    else:
      doneThis[req] = "TRUE"
      # This is the final fix for REQ
      req=re.sub(".+ID=(\d+)\&.+",r'\1',req)
      clearance,clearL = clear.clear(desc)
      loc,lat,lon,keyL = parser.loc(loc,"incadence")
    for i in clearL:
      keyw=keyw+' '+i
    keyw=re.sub('^ ','',keyw)    
    keyWords = keyw + ' ' + keyL
    desc = cleanTag(desc)
    if not re.match("None|^$", clearance):
      wr.writerow([title, appUrl, desc, loc, infoComp, infoDesc, infoSite, infoLogo, infoFace, infoTwit, infoLinked, req, 'UNKNOWN', 'UNKNOWN', lat, lon, infoBeni, job_category, clearance, keyWords,author])
