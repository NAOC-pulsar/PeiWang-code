import fitsio
import sys
import commands
import numpy as np
#from astropy.io import fits
#from astropy.table import Table

if (len(sys.argv)<2):
  print 'Wrong inputs!'
  print 'Usage: python update_Header-OFFSSUB.py fitslist.txt'
  sys.exit()

Fitslist = sys.argv[1]
TotNfile = commands.getoutput('cat fitslist.txt | wc -l')
print 'Go through the list to get a total row number'
Nfile=1

for Line in open(Fitslist):
	Line1=" ".join(Line.split())
	Filename=Line1.replace('\n','').split(" ")[0].strip()
	hdulist = fitsio.FITS(Filename, 'rw')
	hdu1 = hdulist[1]
	header1 = hdu1.read_header()
	Nsub = header1['NAXIS2']
	tbin = header1['TBIN']
	tsub = header1['NSBLK']*tbin
	data = hdu1[:]
	offs_sub = np.zeros((Nsub))
	for isub in range(0, Nsub):
		offs_sub[isub] = tsub * isub + tsub/2.
#	hdu1.write_column('OFFS_SUB', offs_sub)
	hdulist.close()
#	print offs_sub
	print 'Progress:',Nfile, '/', TotNfile, ' ', Filename
	print 'OFFS_SUB[31]=', data['OFFS_SUB'][31], '->', offs_sub[31]
	Nfile=Nfile+1
