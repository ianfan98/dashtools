# curl.py 
# tested with Python 3.4.1
# 2016-03-15 Initial

#! python
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import math
import urllib.request

#sys.stdout.write("Python %s\n" %(sys.version,))
#print('Num of Args=', len(sys.argv), 'argument')
#print('Arg list:', str(sys.argv))
if (len(sys.argv) != 2):
  print("Usage: curl.py url")
  exit()

if (len(sys.argv) == 2):
  print('arg=', sys.argv[1])
  if sys.argv[1].startswith('http'):
    SrcIsURL = True
  else:
    SrcIsURL = False

# read hard-coded mpd file
if(SrcIsURL):
  mpdurl = sys.argv[1]
  #print('src is URL:', mpdurl)
else: #default
  mpdurl='http://q-cdn-cg8-linear-d6b64136.movetv.com/cms/api/channels/176/schedule/now/live.mpd'
f = urllib.request.urlopen(mpdurl)

# TODO http header dump
#info = f.info()
#headerDate = info.get_all('date')
#print('Date from Header: ', headerDate[0])

mpd = f.read()
root = ET.fromstring(mpd.decode('utf-8'))
print(mpd.decode('utf-8'))
exit()