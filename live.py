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
#
# Live Edge
#
def liveEdge(startNumber, timeOffset, segDuration, sugPreDelay, periodDuration):
  print( '  %*s = %*s sec' % (-30, 'timeOffset', -30, timeOffset))
  print( '  %*s = %*s' % (-30, 'startNumber', -30, startNumber))
  print( '  %*s = %*s sec' % (-30, 'sugPreDelay', -30, sugPreDelay))
  if(periodDuration != 'NA'):
    print( '  %*s = %*s sec' % (-30, 'periodDuration', -30, ptTime2Seconds(periodDuration)))
    if( timeOffset < 0):
       print('Content will be available in ', timeOffset, 'sec')
       return
    if( timeOffset > ptTime2Seconds(periodDuration)):
      print('Content is no longer available', timeOffset, 'sec')
      return

  edge = 0;
  edge = startNumber + (timeOffset - sugPreDelay)/segDuration
  MaxIndex = startNumber + (ptTime2Seconds(periodDuration) - sugPreDelay)/segDuration
  
  #print('edge =	', edge, hex(math.floor(edge)))
  #print('Live Edge Segment Index = ', hex(math.floor(edge))[2:])
  print( '  %*s = 0x%08x' % (-30, 'LIVE Edge Segment Index', math.floor(edge)))
  print( '  %*s = 0x%08x' % (-30, 'startNumber', startNumber))
  print( '  %*s = 0x%08x' % (-30, 'Max Segment Index', math.floor(MaxIndex)))
  return

def epoTime(isoTime):
  #tmp = datetime.strptime(isoTime, '%Y-%m-%dT%H:%M:%SZ')
  isoTime = isoTime.strip('Z') 
  tmp = datetime.strptime(isoTime, '%Y-%m-%dT%H:%M:%S')
 # newt = (tmp[0], tmp[1], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7],tmp[8],0)
 # epo = time.mktime(newt)
  return tmp

#PT time format 'PTxxxxxHxxxxMxxxxS'
# return second from PT time
# input can be PT30S, PT4M, PT4M30S, PT2.04800000S, PT20082.815918S
#
def ptTime2Seconds(ptTime):
  pt = ptTime
  # shift to left, ie. remove leading PT
  pt = pt[2:]

  # find H
  ret = pt.find('H')
  if ret != -1:
    hours = pt[:ret]
  # shift out hours
    pt = pt[ret+1:]
  else:
    hours = 0

  # find M
  ret = pt.find('M')
  if ret != -1:
    mins = pt[:ret]
    pt = pt[ret+1:]
  else:
    mins = 0
  # find S
  ret = pt.find('S')
  if ret != -1:
    secs = pt[:ret]
    pt = pt[ret+1:]
  else:
    secs = 0

  totalseconds = 3600*float(hours) + 60*float(mins) + float(secs)
  return totalseconds


def doSegmentTemplate(mpd_ast, mpd_aet, mpd_spd, period_duration):
  
  # attributes from Period SegmentTemplate

  # use full name
  ns = mpd_xmlns + 'SegmentTemplate'
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
      print( '  %*s = %*s' % (-30, 'presentationTimeOffset', -30, st.attrib['presentationTimeOffset']))
     
    sn = int(st.attrib['startNumber'])
    print( '  %*s = %*s' % (-30, 'Segment Duration', -30, st_time))
    print( '  %*s = %*s' % (-30, 'StartNumber', -30, sn))

    t2 = datetime.utcnow()

    print( '  %*s = %*s' % (-30, 'Time NOW from Client', -30, t2.isoformat()))
    if(h_datetime != 'NA'):
      print( '  %*s = %*s' % (-30, 'Time NOW from Server', -30, h_datetime.isoformat()))
    print( '  %*s = %*s' % (-30, 'availabilityStartTime', -30, mpd_ast))

    #t1 = datetime.strptime(mpd_ast, '%Y-%m-%dT%H:%M:%SZ') # not all has Z in it
    if(mpd_ast != 'NA'):
      mpd_ast = mpd_ast.strip('Z') 
      t1 = datetime.strptime(mpd_ast, '%Y-%m-%dT%H:%M:%S')
    d = t2 - t1
    timeOffset = d.total_seconds()
    #print( '  %*s = %*s' % (-30, 'timeOffset', -30, timeOffset))

    if mpd_aet != 'NA':
      mpd_aet = mpd_aet.strip('Z') 
      t3 = datetime.strptime(mpd_aet, '%Y-%m-%dT%H:%M:%S')
      d = t3 - t1
     # print('availability window size=', d.total_seconds(), ' sec ')
      print( '  %*s = %*s seconds' % (-30, 'availability window', -10, d.total_seconds()))
    
    if timeOffset > 0 :
      if(mpd_spd != 'NA'):
        val = ptTime2Seconds(mpd_spd)
      else:
        val = 0 
      liveEdge(sn, timeOffset, st_time, val, period_duration)
      # progress
      if(period_duration != 'NA'):
        print( '  Playback progress now ', round(100*timeOffset/ptTime2Seconds(period_duration)) , '%')
    else:
      print( '  %*s = %*s seconds' % (-30, 'Content Available in', -10, -timeOffset))
      
  return



#sys.stdout.write("Python %s\n" %(sys.version,))
#print('Num of Args=', len(sys.argv), 'argument')
#print('Arg list:', str(sys.argv))
if (len(sys.argv) != 2):
  print('Usage: \nlive.py <mpd_url | filename>\n For example, live.py http://vm2.dashif.org/livesim/mup_30/testpic_2s/Manifest.mpd')
  print('      or live.py manifest.mpd')
  exit()

if (len(sys.argv) == 2):
  print('arg=', sys.argv[1])
  if sys.argv[1].startswith('http'):
    SrcIsURL = True
  else:
    SrcIsURL = False

# time Now
print('Time Now: ', datetime.now())
print('GMT Time Now: ', datetime.utcnow())

# read hard-coded mpd file
if(SrcIsURL):
  mpdurl = sys.argv[1]
  #print('src is URL:', mpdurl)
  # read from URL
  try: f = urllib.request.urlopen(mpdurl)
  except urllib.error.URLError as e:
    print('URL open error: reason :' + e.reason)
    exit()
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
else: # local file
  mpdfile = sys.argv[1]
  f = open(mpdfile) #print('src is URL Use default')
  buf = f.read()
  f.close()

  tree = ET.parse(mpdfile)
  root = tree.getroot()
  # show MPD
  #print(mp)

  # show MPD
  print(buf)
  h_datetime = 'NA'

# get MPD level attributes
mpd_type = root.attrib['type']
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

# Show Period attributes: id, duration, start
nodePeriod = mpd_xmlns + 'Period'
count=0
for p in root.findall(nodePeriod):
  print( '%*s = %*s' % (-30, 'Period', -30, count))
  count=count+1
  if 'id' in p.attrib:
    period_id = p.attrib['id']
  else: 
    period_id = "NA"

  if 'duration' in p.attrib:
    period_duration = p.attrib['duration']
    print('duration= ', round(ptTime2Seconds(period_duration)/60), 'min')
  else: 
    period_duration = "NA"

  if 'start' in p.attrib:
    period_start = p.attrib['start']
  else: 
    period_start = "NA"
  
  print( '  %*s = %*s' % (-30, 'id', -30, period_id))
  print( '  %*s = %*s' % (-30, 'duration', -30, period_duration))
  print( '  %*s = %*s' % (-30, 'start', -30, period_start))
  doSegmentTemplate(mpd_ast, mpd_aet, mpd_spd, period_duration)
  