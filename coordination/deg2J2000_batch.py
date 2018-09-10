#!/usr/bin/env python
# coding=utf-8

print '# Usage:  $python deg2J2000_batch.py'
print '# Input_file: radec_deg_input.list'

from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np

iput_radec = np.genfromtxt('radec_deg_input.list', dtype='string')
Num_row = int((str(iput_radec[:,0].shape).split(',')[0]).split('(')[1])
RaJ_deg = iput_radec[:,0]  #deg (J2000)
DecJ_deg = iput_radec[:,1] #deg (J2000)

print "RaJ2000_deg | DecJ2000_deg | RaJ2000_hms | DecJ2000_dms | GLJ2000_deg | GBJ2000_deg"

# RaJ2000,DecJ2000
for i in range(0, Num_row):
	aaa = np.float32(RaJ_deg[i])
	bbb = np.float32(DecJ_deg[i])
	c = SkyCoord(ra=aaa*u.degree, dec=bbb*u.degree)
	RaJ_DecJ = c.to_string('hmsdms')
	RaJ2000 = str(RaJ_DecJ).split(' ')[0]
	DecJ2000 = str(RaJ_DecJ).split(' ')[1]
#	print '\n', 'RaJ2000 =', RaJ2000, '  DecJ2000 =', DecJ2000

# GL,GB
	Glb = SkyCoord(ra=aaa*u.degree, dec=bbb*u.degree, frame='icrs')
	GL = Glb.galactic.l.degree
	GB = Glb.galactic.b.degree
	GL = round(float(GL),2)
	GB = round(float(GB),2)

	RaJ2000 = RaJ2000.replace('h',':')
	RaJ2000 = RaJ2000.replace('m',':')
	RaJ2000 = RaJ2000.replace('s','')
	DecJ2000 = DecJ2000.replace('d',':')
	DecJ2000 = DecJ2000.replace('m',':')
	DecJ2000 = DecJ2000.replace('s','')

	print RaJ_deg[i], DecJ_deg[i], RaJ2000, DecJ2000, GL ,GB
