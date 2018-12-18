import fitsio
import sys
import numpy as np
import commands
from decimal import *
#from astropy.io import fits
#from astropy.table import Table

if (len(sys.argv)<2):
  print 'Wrong inputs!'
  print 'Usage: python update_Header-STT_offs.py fitslist.txt'
  sys.exit()

Fitslist = sys.argv[1]
TotNfile = commands.getoutput('cat fitslist.txt | wc -l')
print 'Go through the list to get a total row number'
getcontext().prec = 30
Nfile = 1

for Line in open(Fitslist):
	Line1=" ".join(Line.split())
	Filename=Line1.replace('\n','').split(" ")[0].strip()
	hdulist = fitsio.FITS(Filename, 'rw')
	hdu0 = hdulist[0]
	hdu1 = hdulist[1]
	header0 = hdu0.read_header()
	stt_imjd = np.int(header0['STT_IMJD'])
	stt_smjd = np.int(header0['STT_SMJD'])
	stt_offs = Decimal(header0['STT_OFFS'])
	header1 = hdu1.read_header()
	nline = header1['NAXIS2']
	nsblk = header1['NSBLK']
	tbin = Decimal(header1['TBIN'])

	if(Nfile==1):
		if(stt_offs<0.01):
			stt_offs_start = np.int(0)
		elif(stt_offs>0.99):
			stt_offs_start = np.int(0)
			stt_smjd_start = np.int(stt_smjd + 1)
		else:
			print 'STT_OFFS NOT counting from integer seconds!'
			sys.exit()
		stt_imjd_start = np.int(stt_imjd)
		stt_smjd_start = np.int(stt_smjd)		

	T_file = nline*nsblk*tbin
	stt_imjd_updated = stt_imjd_start + np.int((Nfile-1)*T_file/86400)
	stt_smjd_updated = stt_smjd_start + np.int((Nfile-1)*T_file)
	stt_offs_updated = stt_offs_start + np.int(Nfile-1)*Decimal(T_file) - np.int(np.int(Nfile-1)*Decimal(T_file))
	if(stt_offs_updated>1):
		stt_smjd_updated = stt_smjd_updated + 1.
		stt_offs_updated = stt_offs_updated - 1.

	hdu0.write_key('STT_IMJD', stt_imjd_updated)
	hdu0.write_key('STT_SMJD', stt_smjd_updated)
	hdu0.write_key('STT_OFFS', stt_offs_updated)
#	data = hdu1[:]
#	offs_sub = data['OFFS_SUB']*4.
#	hdu1.write_key('OFFS_SUB', offs_sub)
#	hdu1.write_column('OFFS_SUB', offs_sub)
	hdulist.close()
	print 'Progress:',Nfile, '/', TotNfile, ' ', Filename, '\n', 'STT_offs=', stt_offs,'->', stt_offs_updated, 'Delta_offs=', stt_offs_updated-stt_offs
	print 'STT_imjd=', stt_imjd,'->', stt_imjd_updated
	print 'STT_smjd=', stt_smjd,'->', stt_smjd_updated, '\n'
#	print 'OFFS_SUB[255]=', data['OFFS_SUB'][255], '->', offs_sub[255]
	Nfile=Nfile+1
