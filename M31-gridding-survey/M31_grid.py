#!/usr/bin/env python
# coding=utf-8

# Wangpei, Ver.20181217
# $python M31_grid.py grid.txt
# Format of grid.txt: "gridpoint | offset_RaJ(arcmin) | offset_DecJ(arcmin)"

import sys
import datetime as dt
import commands
import numpy as np
from datetime import datetime


##########################################
############### Parameters ###############

# M31 central coordnation
M31raJ = '00:42:44.3'
M31decJ = '41:16:09.0'

# Be set as pointing of P10-N1-M06 (arcmin)
OffsetP10N1M01raJ = '2.59'
OffsetP10N1M01decJ = '-5.11'
##########################################



if (len(sys.argv)<2):
  print '\n', 'Wrong inputs!'
  print 'Usage: python M31_grid.py grid.txt', '\n'
  sys.exit()

Pointlist = sys.argv[1]
TotNpoint = commands.getoutput('cat grid.txt | wc -l')
print 'Go through the list to get a total row number'
Npoint=1

M31DecJ_d = str(M31decJ).split(':')[0]
M31DecJ_m = str(M31decJ).split(':')[1]
M31DecJ_s = str(M31decJ).split(':')[2]
Dec_flag = M31DecJ_d.find('-')
if (int(Dec_flag) == 0 ):
	M31DecJ_rad = (float(M31DecJ_d)-float(M31DecJ_m)/60.-float(M31DecJ_s)/3600.)/180*np.pi
else:
	M31DecJ_rad = (float(M31DecJ_d)+float(M31DecJ_m)/60.+float(M31DecJ_s)/3600.)/180*np.pi


# StartRaJ
OffsetP10N1M01raJ = str(float(OffsetP10N1M01raJ)/15/np.cos(M31DecJ_rad+float(OffsetP10N1M01decJ)/60/180*np.pi))
OffsetP10N1M01raJm = int(OffsetP10N1M01raJ.split(".")[0])
Offra_flag = str(OffsetP10N1M01raJ).find('-')
if (int(Offra_flag) == 0 ):
	OffsetP10N1M01raJs = -1.*float('0.'+OffsetP10N1M01raJ.split(".")[1])*60.
else:
	OffsetP10N1M01raJs = float('0.'+OffsetP10N1M01raJ.split(".")[1])*60.

M31RaJ = datetime.strptime(M31raJ,"%H:%M:%S.%f")
StartRaJ = M31RaJ + dt.timedelta(hours=0,minutes=OffsetP10N1M01raJm,seconds=OffsetP10N1M01raJs)
StartRaJ = str(StartRaJ).split(' ')[1]
print 'StartRaJ =', StartRaJ
StartRaJ = datetime.strptime(StartRaJ,"%H:%M:%S.%f")


# StartDecJ
OffsetP10N1M01decJm = int(OffsetP10N1M01decJ.split(".")[0])
Offdec_flag = str(OffsetP10N1M01decJ).find('-')
if (int(Offdec_flag) == 0 ):
	OffsetP10N1M01decJs = -1.*float('0.'+OffsetP10N1M01decJ.split(".")[1])*60.
else:
	OffsetP10N1M01decJs = float('0.'+OffsetP10N1M01decJ.split(".")[1])*60.

M31H1decJ = datetime.strptime('01:'+M31DecJ_m+':'+M31DecJ_s,"%H:%M:%S.%f")       # H01 assumed
StartDecJ = M31H1decJ + dt.timedelta(hours=0,minutes=OffsetP10N1M01decJm,seconds=OffsetP10N1M01decJs)
OffH1 = int((str(StartDecJ).split(' ')[1]).split(':')[0])
if (OffH1 < 1):
	StartDecJ = str(int(M31DecJ_d)-1)+':'+(str(StartDecJ).split(' ')[1]).split(':')[1]+':'+(str(StartDecJ).split(' ')[1]).split(':')[2]
else:
	StartDecJ = M31DecJ_d+':'+(str(StartDecJ).split(' ')[1]).split(':')[1]+':'+(str(StartDecJ).split(' ')[1]).split(':')[2]

print 'StartDecJ =',StartDecJ, '\n'
StartDecJ_d = str(StartDecJ).split(':')[0]
StartDecJ_m = str(StartDecJ).split(':')[1]
StartDecJ_s = str(StartDecJ).split(':')[2]
StartDec_flag = StartDecJ_d.find('-')
if (int(Dec_flag) == 0 ):
	StartDecJ_rad = (float(StartDecJ_d)-float(StartDecJ_m)/60.-float(StartDecJ_s)/3600.)/180*np.pi
else:
	StartDecJ_rad = (float(StartDecJ_d)+float(StartDecJ_m)/60.+float(StartDecJ_s)/3600.)/180*np.pi


# Generate grid
for Line in open(Pointlist):
	Line1=" ".join(Line.split())
	Sname=Line1.replace('\n','').split(" ")[0].strip()
	OffsetRaJ=Line1.replace('\n','').split(" ")[1].strip()
	OffsetDecJ=Line1.replace('\n','').split(" ")[2].strip()
	OffsetDecJ_rad=float(OffsetDecJ)/60/180*np.pi

	# N1RaJ
	OffsetN1RaJ = str(float(OffsetRaJ)/15/np.cos(StartDecJ_rad+OffsetDecJ_rad))
	OffsetN1raJm = int(OffsetN1RaJ.split(".")[0])
	OffN1ra_flag = str(OffsetN1RaJ).find('-')
	if (int(OffN1ra_flag) == 0 ):
		OffsetN1raJs = -1.*float('0.'+OffsetN1RaJ.split(".")[1])*60.
	else:
		OffsetN1raJs = float('0.'+OffsetN1RaJ.split(".")[1])*60.
	N1RaJ = StartRaJ + dt.timedelta(hours=0, minutes=OffsetN1raJm, seconds=OffsetN1raJs)
	N1RaJ = str(N1RaJ).split(' ')[1]

	# N1DecJ
	OffsetN1decJm = int(OffsetDecJ.split(".")[0])
	OffN1dec_flag = str(OffsetDecJ).find('-')
	if (int(OffN1dec_flag) == 0 ):
		OffsetN1decJs = -1.*float('0.'+OffsetDecJ.split(".")[1])*60.
	else:
		OffsetN1decJs = float('0.'+OffsetDecJ.split(".")[1])*60.
	StartdecJ = datetime.strptime('05:'+StartDecJ_m+':'+StartDecJ_s,"%H:%M:%S.%f")       # H05 assumed
	N1H1DecJ = StartdecJ + dt.timedelta(hours=0,minutes=OffsetN1decJm,seconds=OffsetN1decJs)
	OffN1H1 = int((str(N1H1DecJ).split(' ')[1]).split(':')[0])
	N1DecJ = str(int(StartDecJ_d)+OffN1H1-5)+':'+(str(N1H1DecJ).split(' ')[1]).split(':')[1]+':'+(str(N1H1DecJ).split(' ')[1]).split(':')[2]


	# N2RaJ
	OffsetN2RaJ = float(OffsetRaJ)-1.5
	OffsetN2RaJ = str(float(OffsetN2RaJ)/15/np.cos(StartDecJ_rad+OffsetDecJ_rad+ 2.6/60/180*np.pi))
	OffsetN2raJm = int(OffsetN2RaJ.split(".")[0])
	OffN2ra_flag = str(OffsetN2RaJ).find('-')
	if (int(OffN2ra_flag) == 0 ):
		OffsetN2raJs = -1.*float('0.'+OffsetN2RaJ.split(".")[1])*60.
	else:
		OffsetN2raJs = float('0.'+OffsetN2RaJ.split(".")[1])*60.
	N2RaJ = StartRaJ + dt.timedelta(hours=0, minutes=OffsetN2raJm, seconds=OffsetN2raJs)
	N2RaJ = str(N2RaJ).split(' ')[1]

	# N2DecJ
	OffsetN2DecJ = str(float(OffsetDecJ)+2.6)
	OffsetN2decJm = int(OffsetN2DecJ.split(".")[0])
	OffN2dec_flag = str(OffsetN2DecJ).find('-')
	if (int(OffN2dec_flag) == 0 ):
		OffsetN2decJs = -1.*float('0.'+OffsetN2DecJ.split(".")[1])*60.
	else:
		OffsetN2decJs = float('0.'+OffsetN2DecJ.split(".")[1])*60.
	N2H1DecJ = StartdecJ + dt.timedelta(hours=0,minutes=OffsetN2decJm,seconds=OffsetN2decJs)
	OffN2H1 = int((str(N2H1DecJ).split(' ')[1]).split(':')[0])
	N2DecJ = str(int(StartDecJ_d)+OffN2H1-5)+':'+(str(N2H1DecJ).split(' ')[1]).split(':')[1]+':'+(str(N2H1DecJ).split(' ')[1]).split(':')[2]


	# N3RaJ
	OffsetN3RaJ = str(float(OffsetRaJ)+1.5)
	OffsetN3RaJ = str(float(OffsetN3RaJ)/15/np.cos(StartDecJ_rad+OffsetDecJ_rad+ 2.6/60/180*np.pi))
	OffsetN3raJm = int(OffsetN3RaJ.split(".")[0])
	OffN3ra_flag = str(OffsetN3RaJ).find('-')
	if (int(OffN3ra_flag) == 0 ):
		OffsetN3raJs = -1.*float('0.'+OffsetN3RaJ.split(".")[1])*60.
	else:
		OffsetN3raJs = float('0.'+OffsetN3RaJ.split(".")[1])*60.
	N3RaJ = StartRaJ + dt.timedelta(hours=0, minutes=OffsetN3raJm, seconds=OffsetN3raJs)
	N3RaJ = str(N3RaJ).split(' ')[1]

	# N3DecJ
	N3DecJ = N2DecJ


	# N4RaJ
	OffsetN4RaJ = str(float(OffsetRaJ)+3.0)
	OffsetN4RaJ = str(float(OffsetN4RaJ)/15/np.cos(StartDecJ_rad+OffsetDecJ_rad))
	OffsetN4raJm = int(OffsetN4RaJ.split(".")[0])
	OffN4ra_flag = str(OffsetN4RaJ).find('-')
	if (int(OffN4ra_flag) == 0 ):
		OffsetN4raJs = -1.*float('0.'+OffsetN4RaJ.split(".")[1])*60.
	else:
		OffsetN4raJs = float('0.'+OffsetN4RaJ.split(".")[1])*60.
	N4RaJ = StartRaJ + dt.timedelta(hours=0, minutes=OffsetN4raJm, seconds=OffsetN4raJs)
	N4RaJ = str(N4RaJ).split(' ')[1]

	# N4 DecJ
	N4DecJ = N1DecJ

	print '\n', 'Source:', Npoint, 'of', TotNpoint, ' ', Sname
	print '------------------------------------------------'
	print str(Sname)+'(RaJ2000,DecJ2000) =', N1RaJ, ' ', N1DecJ, '\n'
	print 'N1 | RA+0.0arcmin_DEC+0.0arcmin =', N1RaJ, ' ', N1DecJ
	print 'N2 | RA-1.5arcmin_DEC+2.6arcmin =', N2RaJ, ' ', N2DecJ
	print 'N3 | RA+1.5arcmin_DEC+2.6arcmin =', N3RaJ, ' ', N3DecJ
	print 'N4 | RA+3.0arcmin_DEC+0.0arcmin =', N4RaJ, ' ', N4DecJ, '\n'
	Npoint=Npoint+1
