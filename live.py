# MPEG DASH MPD live edge calculator
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
  print('Usage: \nlive.py mpd_url\n For example, live.py http://vm2.dashif.org/livesim/mup_30/testpic_2s/Manifest.mpd')
  exit()

if (len(sys.argv) == 2):
  print('arg=', sys.argv[1])
  if sys.argv[1].startswith('http'):
    SrcIsURL = True
  else:
    SrcIsURL = False

def liveEdge(startNumber, timeOffset, segDuration, sugPreDelay):
  edge = 0;
  edge = startNumber + (timeOffset-sugPreDelay)/segDuration
  #print('edge =	', edge, hex(math.floor(edge)))
  #print('Live Edge Segment Index = ', hex(math.floor(edge))[2:])
  print( '%*s = 0x%*s' % (-30, 'LIVE Edge Segment Index', -30, hex(math.floor(edge))[2:]))
  return

def epoTime(isoTime):
  #tmp = datetime.strptime(isoTime, '%Y-%m-%dT%H:%M:%SZ')
  isoTime = isoTime.strip('Z') 
  tmp = datetime.strptime(isoTime, '%Y-%m-%dT%H:%M:%S')
 # newt = (tmp[0], tmp[1], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7],tmp[8],0)
 # epo = time.mktime(newt)
  return tmp

# return second from PT time
# input can be PT30S, PT4M, PT4M30S, PT2.04800000S, PT20082.815918S
#
def getSec(ptTime):
  val = 2
  return val 

# time Now
print('Time Now: ', datetime.now())
print('GMT Time Now: ', datetime.utcnow())

# read hard-coded mpd file
if(SrcIsURL):
  mpdurl = sys.argv[1]
  #print('src is URL:', mpdurl)
else: #default
  mpdurl='http://q-cdn-cg8-linear-d6b64136.movetv.com/cms/api/channels/176/schedule/now/live.mpd'
  #print('src is URL Use default')

#tree = ET.parse('wowza.mpd')
#root = tree.getroot()

# read from URL
#mpdurl= 'https://wowzaec2demo.streamlock.net/live/bigbuckbunny/manifest_mpm4sav_mvnumber.mpd'
#mpdurl='http://q-cdn-cg8-linear-d6b64136.movetv.com/cms/api/channels/176/schedule/now/live.mpd'
f = urllib.request.urlopen(mpdurl)
info = f.info()
headerDate = info.get_all('date')
print('Date from Header: ', headerDate[0])
# TODO Date format from HTTP is RFC 1123, e.g. "Wed, 16 Mar 2016 22:20:28 GMT"
# Need to construct datetime object
h_datetime =  datetime.strptime(headerDate[0], '%a, %d %b %Y %H:%M:%S GMT')
print('Date from Header ISO format: ', h_datetime.isoformat())

mpd = f.read()
root = ET.fromstring(mpd.decode('utf-8'))

# show MPD
print(mpd.decode('utf-8'))

# get MPD level attributes

mpd_type=root.attrib['type']
if 'minimumUpdatePeriod' in root.attrib:
  mpd_mup = root.attrib['minimumUpdatePeriod']
else:
  mpd_mup = "NA"

if 'publishTime' in root.attrib:
  mpd_pt=root.attrib['publishTime']
else: 
  mpd_pt='NA' 

if 'mediaPresentationDuration' in root.attrib:
  mpd_mpd = root.attrib['mediaPresentationDuration']
else:
  mpd_mpd = 'NA'

if 'availabilityStartTime' in root.attrib: 
  mpd_ast=root.attrib['availabilityStartTime']
else:
  mpd_ast = "NA"

if 'availabilityEndTime' in root.attrib:
  mpd_aet=root.attrib['availabilityEndTime']
else:
  mpd_aet = 'NA'

if 'timeShiftBufferDepth' in root.attrib:
  mpd_tsbd=root.attrib['timeShiftBufferDepth']
else:
  mpd_tsbd = 'NA'

if 'suggestedPresentationDelay' in root.attrib:
  mpd_spd=root.attrib['suggestedPresentationDelay']
else: 
  mpd_spd = "NA"
mpd_mbt=root.attrib['minBufferTime']
mpd_xmlns = root.tag #tag for namespace?
if mpd_xmlns.endswith('MPD'):
  mpd_xmlns = mpd_xmlns[:-3] # remove trailing MPD

print( '%*s = %*s' % (-30, 'type', -30, mpd_type))
print( '%*s = %*s' % (-30, 'minimumUpdatePeriod =', -30, mpd_mup))
print( '%*s = %*s' % (-30, 'publishTime', -30, mpd_pt))
print( '%*s = %*s' % (-30, 'availabilityStartTime', -30, mpd_ast))
print( '%*s = %*s' % (-30, 'availabilityEndTime', -30, mpd_aet))
print( '%*s = %*s' % (-30, 'timeShiftBufferDepth', -30, mpd_tsbd))
print( '%*s = %*s' % (-30, 'suggestedPresentationDelay', -30, mpd_spd))
print( '%*s = %*s' % (-30, 'minBufferTime', -30, mpd_mbt))
print( '%*s = %*s' % (-30, 'mediaPresentationDuration', -30, mpd_mpd))

# check if it is LIVE or VOD
if mpd_ast == 'NA':
  print("***  NOT LIVE Service  ***")
  exit()

# convert iso time to unix epo
#mpd_pt_epo = time.mktime(time.strptime(mpd_pt, '%Y-%m-%dT%H:%M:%SZ'))
#mpd_ast_epo = time.mktime(time.strptime(mpd_ast, '%Y-%m-%dT%H:%M:%SZ'))
if mpd_ast != 'NA':
  mpd_ast_epo = epoTime(mpd_ast)

#print('pt_epo=', mpd_pt_epo)
#print('ast_epo=', mpd_ast_epo)

# get relative time
mpd_mup_f = getSec(mpd_mup)
mpd_tsbd_f = getSec(mpd_tsbd)
if(mpd_spd != 'NA'):
  mpd_spd_f = getSec(mpd_spd)
else:
  mpd_spd_f = 0;
mpd_mbt_f = getSec(mpd_mbt)

#print(mpd_mup_f,mpd_tsbd_f,mpd_spd_f,mpd_mbt_f) 


# attributes from Period SegmentTemplate

# sling ns
ns = mpd_xmlns + 'SegmentTemplate'
#print('ns=', ns)

# wowza ns
#ns = '{urn:mpeg:dash:schema:mpd:2011}SegmentTemplate'
for st in root.iter(ns):
  ts = 1.0
  if 'timescale' in st.attrib:
    ts = float(st.attrib['timescale'])
  else:
    ts = 1.0
  if 'duration' in st.attrib:
    st_time = float(st.attrib['duration'])/ts
  else:
    st_time = 1

  if 'presentationTimeOffset' in st.attrib:
    print( '%*s = %*s' % (-30, 'presentationTimeOffset', -30, st.attrib['presentationTimeOffset']))
   
  sn = int(st.attrib['startNumber'])
  print( '%*s = %*s' % (-30, 'Segment Duration', -30, st_time))
  print( '%*s = %*s' % (-30, 'StartNumber', -30, sn))

  t2 = datetime.utcnow()

  print( '%*s = %*s' % (-30, 'Time NOW from Client', -30, t2.isoformat()))
  print( '%*s = %*s' % (-30, 'Time NOW from Server', -30, h_datetime.isoformat()))
  print( '%*s = %*s' % (-30, 'availabilityStartTime', -30, mpd_ast))

  #t1 = datetime.strptime(mpd_ast, '%Y-%m-%dT%H:%M:%SZ') # not all has Z in it
  mpd_ast = mpd_ast.strip('Z') 
  t1 = datetime.strptime(mpd_ast, '%Y-%m-%dT%H:%M:%S')
  d = t2 -t1
  timeOffset = d.total_seconds()
  print( '%*s = %*s' % (-30, 'timeOffset', -30, timeOffset))

  liveEdge(sn, timeOffset, st_time,mpd_spd_f)
