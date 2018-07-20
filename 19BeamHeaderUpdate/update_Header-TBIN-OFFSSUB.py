import fitsio
import sys
import commands
#from astropy.io import fits
#from astropy.table import Table

if (len(sys.argv)<2):
  print 'Wrong inputs!'
  print 'Usage: python update_TBIN.py fitslist.txt'
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
	tbin = header1['TBIN']
	tbin_updated = tbin*4.
	hdu1.write_key('TBIN', tbin_updated)
	data = hdu1[:]
	offs_sub = data['OFFS_SUB']*4.
#	hdu1.write_key('OFFS_SUB', offs_sub)
	hdu1.write_column('OFFS_SUB', offs_sub)
	hdulist.close()
	print 'Progress:',Nfile, '/', TotNfile, ' ', Filename, 'TBIN=',tbin,'->',tbin_updated
	print 'OFFS_SUB[255]=', data['OFFS_SUB'][255], '->', offs_sub[255]
	Nfile=Nfile+1
