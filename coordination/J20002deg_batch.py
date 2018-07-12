#!/usr/bin/env python
# coding=utf-8

import numpy as np
import sys
from astropy.coordinates import SkyCoord
from astropy import units as u

iput_radec=np.genfromtxt('radec_dms_input.list', dtype='string')
Num_row = int((str(iput_radec[:,0].shape).split(',')[0]).split('(')[1])
RaJ=iput_radec[:,0]  #hh:mm:ss (J2000)
DecJ=iput_radec[:,1] #dd:mm:ss (J2000)

print '\n',"RaJ2000 | DecJ2000 | RaJ2000_deg | DecJ2000_deg | GLJ2000 | GBJ2000 | GLJ2000_deg | GBJ2000_deg"

# Ra,Dec
for i in range(0, Num_row):
	RaJ_h = str(RaJ[i]).split(':')[0]
	RaJ_m = str(RaJ[i]).split(':')[1]
	RaJ_s = str(RaJ[i]).split(':')[2]
	RaJ_hms = str(RaJ_h)+'h'+str(RaJ_m)+'m'+str(RaJ_s)+'s'
	RaJ2000 = str(RaJ_h)+':'+str(RaJ_m)+':'+str(RaJ_s)
	DecJ_d = str(DecJ[i]).split(':')[0]
	DecJ_m = str(DecJ[i]).split(':')[1]
	DecJ_s = str(DecJ[i]).split(':')[2]
	DecJ_dms = str(DecJ_d)+'d'+str(DecJ_m)+'m'+str(DecJ_s)+'s'
	DecJ2000 = str(DecJ_d)+':'+str(DecJ_m)+':'+str(DecJ_s)
	RaJ_deg = (str(SkyCoord(RaJ_hms, DecJ_dms, frame='icrs')).split('(')[3]).split(',')[0]
	Dec_flag = DecJ_d.find('-')
	if (int(Dec_flag) == 0 ):
		DecJ_deg = float(DecJ_d)-float(DecJ_m)/60.-float(DecJ_s)/3600.
	else:
		DecJ_deg = float(DecJ_d)+float(DecJ_m)/60.+float(DecJ_s)/3600.

	if (int(Dec_flag) == 0 and int(DecJ_d) == 0):
		DecJ_deg = '-'+str(DecJ_deg)

# GL,GB
	Glb = SkyCoord(ra=float(RaJ_deg)*u.degree, dec=float(DecJ_deg)*u.degree, frame='icrs')
	GL = Glb.galactic.l.degree
	GB = Glb.galactic.b.degree
	GL = round(float(GL),2)
	GB = round(float(GB),2)
	GLJ = Glb.galactic.l
	GBJ = Glb.galactic.b
	
	print RaJ2000,DecJ2000,RaJ_deg,DecJ_deg,GLJ,GBJ,GL,GB
print '\n'
#	print '\n', 'Ra(J2000) =', RaJ, '  Dec(J2000) =', DecJ, '  Ra(deg) =', RaJ_deg, '  Dec(deg) =', DecJ_deg, '  GL(J2000) =', GLJ, '   GB(J2000) =', GBJ, '  GL(deg) =', GL, '   GB(deg) =', GB, '\n'
