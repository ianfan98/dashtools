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
  print("Usage: curl.py <url>")
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
  mpdurl='http://dash.edgesuite.net/dash264/TestCases/5a/1/manifest.mpd'
f = urllib.request.urlopen(mpdurl)

txt = f.read()
print(txt.decode('utf-8'))
exit()
