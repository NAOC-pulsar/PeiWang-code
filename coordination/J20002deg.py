#!/usr/bin/env python
# coding=utf-8

import sys
from astropy.coordinates import SkyCoord
from astropy import units as u


RaJ = '23:36:36.586975'      # hh:mm:ss (J2000)
DecJ = '-6:29:35.7'    # dd:mm:ss (J2000)


# Ra,Dec
RaJ_h = str(RaJ).split(':')[0]
RaJ_m = str(RaJ).split(':')[1]
RaJ_s = str(RaJ).split(':')[2]
RaJ_hms = str(RaJ_h)+'h'+str(RaJ_m)+'m'+str(RaJ_s)+'s'
DecJ_d = str(DecJ).split(':')[0]
DecJ_m = str(DecJ).split(':')[1]
DecJ_s = str(DecJ).split(':')[2]
DecJ_dms = str(DecJ_d)+'d'+str(DecJ_m)+'m'+str(DecJ_s)+'s'
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

print '\n', 'Ra(J2000) =', RaJ, '  Dec(J2000) =', DecJ, '\n', 'Ra(deg) =', RaJ_deg, '  Dec(deg) =', DecJ_deg, '\n', 'GL(J2000) =', GLJ, '   GB(J2000) =', GBJ, '\n', 'GL(deg) =', format(GL,'.2f'), '   GB(deg) =', format(GB,'.2f'), '\n'
