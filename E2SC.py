#!/usr/bin/env python
# by Ran Novitsky Nof (ran.nof@gmail.com), 2015 @ BSL

# convert E2 and DM event xml to SeisComP3 event xml.
# Seiscomp3 xml can be fed to Seicomp3 database using scdb.
# Examples:
#   E2SC.py -i events_20150214.log -o SCXML   
#   scdb -i SCXML -d mysql://sysop:sysop@localhost/seiscomp3
# or:
#   cat [ELARMSXMLFILE] | E2SC.py | scdb -i - -d mysql://sysop:sysop@localhost/seiscomp3
# or:
#   E2SC.py -i events_*.log | scdb -i - -d mysql://sysop:sysop@localhost/seiscomp3
#
#
#
# ***********************************************************************************
# *    Copyright (C) by Ran Novitsky Nof                                            *
# *                                                                                 *
# *    E2SC.py is free software: you can redistribute it and/or modify              *
# *    it under the terms of the GNU Lesser General Public License as published by  *
# *    the Free Software Foundation, either version 3 of the License, or            *
# *    (at your option) any later version.                                          *
# *                                                                                 *
# *    This program is distributed in the hope that it will be useful,              *
# *    but WITHOUT ANY WARRANTY; without even the implied warranty of               *
# *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                *
# *    GNU Lesser General Public License for more details.                          *
# *                                                                                 *
# *    You should have received a copy of the GNU Lesser General Public License     *
# *    along with this program.  If not, see <http://www.gnu.org/licenses/>.        *
# ***********************************************************************************


import datetime,argparse,sys,os
from xml.dom import minidom

# command line parser

def is_valid_outfile(parser, arg):
    if arg=='-':
      return sys.stdout
    if os.path.exists(arg):
      parser.error("The file %s exist!" % arg)
    else:
      try:
        f = open(arg, 'w')
      except Exception,msg:
        parser.error(msg.message)
      return open(arg, 'w')  # return an open file handle

parser = argparse.ArgumentParser(
         formatter_class=argparse.RawDescriptionHelpFormatter,
         description='''E2SC - ElarmS to SeisComP3 event xml converter''',
         epilog='''Created by Ran Novitsky Nof (ran.nof@gmail.com), 2015 @ BSL''')
parser.add_argument('-o',metavar='OutXML',default='-',help='Output xml file (SeisComP3)',type=lambda x:is_valid_outfile(parser, x) )
parser.add_argument('-i',metavar='InXML',nargs='+',default='-',help='input xml file(s) (ElarmS)',type=argparse.FileType('r'))
parser.add_argument('-t',action='store_true',help='Test mode (ignors input parameter if applicable)',default=False)

def XE2S(Eid,ot,msgtime,mag,lat,lon,depth,agency='GII',author='EEWS',otu=0,magUnit='M',magu=0,latu=0,lonu=0,depthu=0,now=datetime.datetime.utcnow()):
  mag,lat,lon,depth,otu,magu,latu,lonu,depthu = [str(i) for i in mag,lat,lon,depth,otu,magu,latu,lonu,depthu] # convert values to strings
  xmlexampl ='''    <origin publicID="Origin#'''+now.strftime("%Y%m%d%H%M%S.%f")+'''">
      <time>
        <value>'''+ot.isoformat()+'Z'+'''</value>
        <uncertainty>'''+otu+'''</uncertainty>
      </time>
      <latitude>
        <value>'''+lat+'''</value>
        <uncertainty>'''+latu+'''</uncertainty>
      </latitude>
      <longitude>
        <value>'''+lon+'''</value>
        <uncertainty>'''+lonu+'''</uncertainty>
      </longitude>
      <depth>
        <value>'''+depth+'''</value>
        <uncertainty>'''+depthu+'''</uncertainty>
      </depth>
      <creationInfo>
        <agencyID>'''+agency+'''</agencyID>
        <author>'''+author+'''</author>
        <creationTime>'''+msgtime.isoformat()+'Z'+'''</creationTime>
      </creationInfo>     
      <magnitude publicID="Origin#'''+now.strftime("%Y%m%d%H%M%S.%f")+'''#netMag.M">
        <magnitude>
          <value>'''+mag+'''</value>
          <uncertainty>'''+magu+'''</uncertainty>
        </magnitude>
        <type>'''+magUnit+'''</type>
        <creationInfo>
          <agencyID>'''+agency+'''</agencyID>
          <author>'''+author+'''</author>
          <creationTime>'''+msgtime.isoformat()+'Z'+'''</creationTime>
        </creationInfo>        
      </magnitude>
    </origin>  
    <event publicID="'''+Eid+'''">
      <preferredOriginID>Origin#'''+now.strftime("%Y%m%d%H%M%S.%f")+'''</preferredOriginID>
      <preferredMagnitudeID>Origin#'''+now.strftime("%Y%m%d%H%M%S.%f")+'''#netMag.M</preferredMagnitudeID>
      <originReference>Origin#'''+now.strftime("%Y%m%d%H%M%S.%f")+'''</originReference>
      <creationInfo>
        <agencyID>'''+agency+'''</agencyID>
        <author>'''+author+'''</author>
        <creationTime>'''+msgtime.isoformat()+'Z'+'''</creationTime>
      </creationInfo>      
    </event>'''    
  return xmlexampl
  
def getDMxmlmsg(Eid,mag,lat,lon,depth,delay):
  now = datetime.datetime.utcnow()
  T = (now-datetime.timedelta(0,delay)).isoformat()[:-3]
  xmlexampl ='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<event_message alg_vers="2.0.11 2014-04-08" category="live" instance="DM@EEWS" message_type="new" orig_sys="elarms" timestamp="'''+now.isoformat()[:-3]+'''Z" version="0">

  <core_info id="'''+Eid+'''">
    <mag units="Mw">'''+str(mag)+'''</mag>
    <mag_uncer units="Mw">0.3982</mag_uncer>
    <lat units="deg">'''+str(lat)+'''</lat>
    <lat_uncer units="deg">0.1283</lat_uncer>
    <lon units="deg">'''+str(lon)+'''</lon>
    <lon_uncer units="deg">0.1283</lon_uncer>
    <depth units="km">'''+str(depth)+'''</depth>
    <depth_uncer units="km">1.0000</depth_uncer>
    <orig_time units="UTC">'''+T+'''Z</orig_time>
    <orig_time_uncer units="sec">2.5177</orig_time_uncer>
    <likelihood>0.9091</likelihood>
  </core_info>

</event_message>'''
  return xmlexampl


def getE2xmlmsg(Eid,mag,lat,lon,depth,delay):
  now = datetime.datetime.utcnow()
  T = (now-datetime.timedelta(0,delay)).isoformat()[:-3]
  xmlexampl ='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<event_message alg_vers="2.4.1 2014-03-04" category="live" instance="E2@EEWS" message_type="new" orig_sys="elarms" timestamp="'''+now.isoformat()[:-3]+'''Z" version="3">

  <core_info id="'''+Eid+'''">
    <mag units="Mw">'''+str(mag)+'''</mag>
    <mag_uncer units="Mw">0.3982</mag_uncer>
    <lat units="deg">'''+str(lat)+'''</lat>
    <lat_uncer units="deg">0.1283</lat_uncer>
    <lon units="deg">'''+str(lon)+'''</lon>
    <lon_uncer units="deg">0.1283</lon_uncer>
    <depth units="km">'''+str(depth)+'''</depth>
    <depth_uncer units="km">1.0000</depth_uncer>
    <orig_time units="UTC">'''+T+'''Z</orig_time>
    <orig_time_uncer units="sec">2.5177</orig_time_uncer>
    <likelihood>0.9091</likelihood>
    <num_stations>5</num_stations>
  </core_info>
  
</event_message>'''
  return xmlexampl


class algXML(object):
  def __init__(self,m=None):
    self.type='X'
    self.lat=0.0
    self.latu=0.0
    self.lon=0.0
    self.lonu=0.0
    self.depth=0.0
    self.depthu=0.0
    self.msgtime=datetime.datetime.min
    self.raw = None
    self.Eid = None
    self.msgorigsys = None
    self.msgtype = None
    self.orig_time=datetime.datetime.min
    self.mag=0.0
    self.magu=0.0
    self.magUnit = None
    if m: self.decode(m)
  def decode(self,m):
    self.raw = m
    xmldoc=minidom.parseString(m)
    em = xmldoc.getElementsByTagName('event_message')[0]
    self.Eid=xmldoc.getElementsByTagName('core_info')[0].attributes['id'].value
    self.msgorigsys=em.attributes['orig_sys'].value
    self.instance=em.attributes['instance'].value
    self.msgtime=datetime.datetime.strptime(em.attributes['timestamp'].value,'%Y-%m-%dT%H:%M:%S.%fZ')
    self.msgtype=em.attributes['message_type'].value
    self.lat=float(xmldoc.getElementsByTagName('lat')[0].firstChild.data)
    self.latu=float(xmldoc.getElementsByTagName('lat_uncer')[0].firstChild.data)
    self.lon=float(xmldoc.getElementsByTagName('lon')[0].firstChild.data)
    self.lonu=float(xmldoc.getElementsByTagName('lon_uncer')[0].firstChild.data)
    self.depth=float(xmldoc.getElementsByTagName('depth')[0].firstChild.data)
    self.depthu=float(xmldoc.getElementsByTagName('depth_uncer')[0].firstChild.data)
    self.orig_time=datetime.datetime.strptime(xmldoc.getElementsByTagName('orig_time')[0].firstChild.data,'%Y-%m-%dT%H:%M:%S.%fZ')
    self.orig_timeu=float(xmldoc.getElementsByTagName('orig_time_uncer')[0].firstChild.data)
    self.mag=float(xmldoc.getElementsByTagName('mag')[0].firstChild.data)
    self.magu=float(xmldoc.getElementsByTagName('mag_uncer')[0].firstChild.data)
    self.magUnit=xmldoc.getElementsByTagName('mag')[0].attributes['units'].value
  def __call__(self,m=None):
    if m: self.decode(m)
    return [self.__dict__[k] for k in \
         ["Eid",'orig_time','msgtime','mag','lat','lon','depth',\
         'msgorigsys','instance','orig_timeu','magUnit','magu','latu','lonu','depthu']]\
         +[datetime.datetime.utcnow()]
  def __str__(self):
    return '%s | E: %s (%s - %s) %f %f %f %f%s (%f)'%(self.orig_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),self.Eid,self.msgorigsys,self.msgtype,self.lat,self.lon,self.depth,self.mag,self.magUnit,(self.msgtime-self.orig_time).total_seconds())

def test():
  xml = getE2xmlmsg('test',6.5,31.5,35.5,10,0)
  return xml

def txt2scxml(lines):
  txt = ''  
  eventsXMLs = ['<?'+event for event in (''.join([l for l in lines if l.lstrip().startswith('<')])).split('<?')][1:]  
  for xml in eventsXMLs:
    scxml = algXML(xml)
    txt+=XE2S(*scxml())    
  return txt

def xmlwrap(txt):
  'wrap xml with start and end labels'
  txt = '''<?xml version="1.0" encoding="UTF-8"?>
<seiscomp xmlns="http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.7" version="0.7">
  <EventParameters>
  '''+txt+'''
  </EventParameters>
</seiscomp>'''
  return txt

def Emsg2lines(msg):
  lines = msg.split('\n')
  lines = [line+'\n' for line in lines]
  return lines
  
def lines2scxml(lines):
  txt =  txt2scxml(lines)
  txt = xmlwrap(txt)
  return txt
  
if __name__=='__main__':
  # parse the arguments
  args = parser.parse_args(sys.argv[1:])
  if args.t:
    lines = Emsg2lines(test())
  else:
    lines = []
    for i in args.i:
      lines += i.readlines()
      i.close()
  txt =  lines2scxml(lines)
  args.o.write(txt)
  args.o.close()
