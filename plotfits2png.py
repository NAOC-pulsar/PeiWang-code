#!/usr/bin/env python
import numpy as np  
#import pyfits
import astropy.io.fits as pyfits
import os
import datetime
import time
import sys 
from decimal import Decimal
secperday = 3600 * 24

if (len(sys.argv)==2):
    starttime=datetime.datetime.now()
    print 'record start time:',starttime
else:
    print """
usage: %s filename
This will out put a png file in 
current dir.
          """ % sys.argv[0]

    sys.exit()

filename = sys.argv[1]


hdulist = pyfits.open(filename)
print 'hdu list length', len(hdulist) 
hdu0 = hdulist[0]
hdu1 = hdulist[1]
#hdu2 = hdulist[2]
data1 = hdu1.data['data']
#data2 = hdu2.data
header1 = hdu1.header
print hdu0.header
print hdu1.header
print data1.shape

fchannel = hdulist['SUBINT'].data[0]['DAT_FREQ']
fch1 = fchannel[0]
obsfreq = hdu0.header['OBSFREQ']
obsnchan = hdu0.header['OBSNCHAN']
obsbw = hdu0.header['OBSBW']
fmin = obsfreq - obsbw/2.
fmax = obsfreq + obsbw/2.
nf = obsnchan
df = hdu1.header['CHAN_BW']
tsamp = hdu1.header['TBIN']
nsubint = hdu1.header['NAXIS2']
samppersubint = int(hdu1.header['NSBLK'])
nsamp = nsubint * samppersubint
sourename = hdu0.header['SRC_NAME']
ra = hdu0.header['RA']
dec = hdu0.header['DEC']
#tstart = Decimal("%d.%d" % (hdu0.header['STT_IMJD'], hdu0.header['STT_SMJD']))
subintoffset = hdu1.header['NSUBOFFS']
tstart = "%.13f" % (Decimal(hdu0.header['STT_IMJD']) + Decimal(hdu0.header['STT_SMJD'] + tsamp * samppersubint * subintoffset )/secperday )
nbits = hdu0.header['BITPIX']
header = hdu0.header + hdu1.header
dtype = ''

print 'freq %s MHz, nchan %d, bw %s MHz' % ( obsfreq, obsnchan, obsbw)
print 'MJD:', tstart
print 'fch1, df', fch1, df 
print 'file length %f tsamp %f nsamp %f' %(tsamp*nsamp,tsamp,nsamp)
print 'data.shape:', data1.shape

from pylab import *
from matplotlib.ticker import  MultipleLocator

switch_backend('ps')
a,b,c,d,e = data1.shape
fig = figure(figsize=(16,12*c), dpi=80)
for i in range(c):
    data = data1[:,:,i,:,:].squeeze().reshape((-1,d))
    l, m = data.shape
    data = data.reshape(l/64, 64, d).sum(axis=1)
    bandpass = np.sum(data,axis=0)
    print data.shape
    #data -= data.mean(axis=0).transpose().astype(np.uint64)
    subplotnum=int(str(2*c)+'1'+str(2*i+1))
    ax=fig.add_subplot(subplotnum)
    ax.imshow(data.T, aspect='auto')
    ax.set_ylabel('num of channel  '+'pol'+str(i+1))
    ax.set_xlim(0.,tsamp*nsamp)
    if i < 1 : title(filename.split('/')[-1])
    
    subplotnum=int(str(2*c)+'1'+str(2*i+2))
    ax=fig.add_subplot(subplotnum)
    ax.plot(bandpass)
    ax.set_ylabel('bandpass of '+'pol'+str(i+1))
    ax.set_xlim(0.,obsnchan)
    #colorbar()
    #plot(data.sum(axis=0))
    #plot(data.sum(axis=1))
    #show()
xlabel('time (s)')
imgfilename=(filename.split('/')[-1])[:-5]+'.png'
print "img file name", imgfilename
savefig(imgfilename)
clf()
#if c > 1:
#    data = data1[:,:,0,:,:].squeeze().reshape((-1,d))
#else:
#    data = data1.squeeze().reshape((-1,d))
#l, m = data.shape
#data = data.reshape(l/64, 64, d).sum(axis=1)
#print data.shape
##data -= data.mean(axis=0).transpose().astype(np.uint64)
#
#from pylab import *
#
#switch_backend('ps')
#imshow(data.T, aspect='auto')
##colorbar()
##plot(data.sum(axis=0))
##plot(data.sum(axis=1))
##show()
#
#imgfilename=filename[:-5]+'.png'
#print "img file name", imgfilename
#savefig(imgfilename)

endtime=datetime.datetime.now()
print 'START:',starttime
print 'END:',endtime
print 'DURATION:',(endtime-starttime).seconds,' sec'
