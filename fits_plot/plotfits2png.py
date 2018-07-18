#!/usr/bin/env python
import numpy as np  
#import pyfits
import astropy.io.fits as pyfits
from astropy.time import Time
import os
import datetime as dt
from datetime import datetime
import time
import sys 
import string
from decimal import Decimal
from decimal import getcontext
secperday = 3600 * 24

np.set_printoptions(suppress=True)

#check input
if (len(sys.argv)==2):
    filename=sys.argv[1]

elif (len(sys.argv)==6):
    startn=int(sys.argv[1])
    endn=int(sys.argv[2])
    startfreq=int(sys.argv[3])
    endfreq=int(sys.argv[4])
    filename=sys.argv[5]
    starttime=datetime.now()
    print 'record start time:',starttime
else :
    print 'too few input parameters!'
    print 'example:'
    print 'python *.py startn endn startchan endchan FAST.fits'
    sys.exit()


starttime=datetime.now()
print 'record start time:',starttime

hdulist = pyfits.open(filename)
print 'hdu list length', len(hdulist) 
hdu0 = hdulist[0]
hdu1 = hdulist[1]
#hdu2 = hdulist[2]
data1 = hdu1.data['data']
#data2 = hdu2.data
header1 = hdu1.header
#print hdu0.header
#print hdu1.header
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
#Ultra-wide band receiver
#tstart = "%.13f" % (Decimal(hdu0.header['STT_IMJD']) + Decimal(hdu0.header['STT_SMJD'] + tsamp * samppersubint * subintoffset )/secperday )
#19-beams
tstart = "%.13f" % (Decimal(hdu0.header['STT_IMJD']) + (Decimal(hdu0.header['STT_SMJD']) + Decimal(hdu0.header['STT_OFFS']) )/secperday)
# 

# Transfer Fits header MJD --> UTC time
#Starttime = string.atof(tstart)
Starttime = float(tstart)
t_header = Time(Starttime,format='mjd',scale='utc')
tmp_t_header = str(t_header.datetime).split('.')
if tmp_t_header.__len__() == 1:
    tmp_t_header[0] = tmp_t_header[0] + '.000001'
else:
    tmp_t_header[0] = tmp_t_header[0] + '.' + tmp_t_header[1]

Starttime_utc = datetime.strptime(tmp_t_header[0],"%Y-%m-%d %H:%M:%S.%f")
Starttime_BJ = Starttime_utc + dt.timedelta(hours=8)
print Starttime_BJ

nbits = hdu0.header['BITPIX']
header = hdu0.header + hdu1.header
dtype = ''


#input check 

if (len(sys.argv)==2):
    startn = 0 
    endn = nsubint-1
    startfreq = 0 
    endfreq = nf-1

else:
    if startn < 0 or startn >= endn : 
        startn = 0 
    if endn >= nsubint or endn < 0:
        endn = nsubint-1
    
    if startfreq < 0 or startfreq >= endfreq : 
        startfreq = 0 
    if endfreq >= nf or endfreq < 0:
        endfreq = nf-1


#File information out put
#name, mjd, time, freq

name = 'filename: '+filename.split('/')[-1]
mjd = str('MJD: %s' %(tstart))
time = str('plot length: %s s' % ((endn - startn)*samppersubint*tsamp))
freq = str('plot Frequence: %sMHz - %sMHz' % (fch1+startfreq*df, fch1+endfreq*df))


print 'freq %s MHz, nchan %d, bw %s MHz' % ( obsfreq, obsnchan, obsbw)
print 'MJD:', tstart
print 'fch1, df', fch1, df 
print 'file length %f tsamp %f nsamp %f' %(tsamp*nsamp,tsamp,nsamp)
print 'data.shape:', data1.shape

# ASCII file out
bandpassfilename=(filename.split('/')[-1])[:-5]+'.bandpass'
print "bandpass file name: %s " %(bandpassfilename)


from pylab import *
from matplotlib.ticker import  MultipleLocator

switch_backend('ps')
a,b,c,d,e = data1.shape
d = (endfreq - startfreq)
bandpassout = np.zeros((d,c+1))
for i in range(d): bandpassout[i,0] = fch1+(startfreq+i)*df
fig = figure(figsize=(16,4.5*c), dpi=80)
fig.text(0.1,0.91,name+"\n"+mjd, fontsize = 15)
fig.text(0.5,0.91,time+"\n"+freq, fontsize = 15)
for i in range(c):
    #data = data1[:,:,i,:,:].squeeze().reshape((-1,d))
    data = data1[startn:endn,:,i,startfreq:endfreq,:].squeeze().reshape((-1,d))
    #l, m = data.shape
    #data = data.reshape(l/64, 64, d).sum(axis=1)
    bandpass = np.sum(data,axis=0)
    bandpassout[:,i+1] = bandpass
    print data.shape
    #data -= data.mean(axis=0).transpose().astype(np.uint64)
    #subplotnum=int(str(2*c)+'1'+str(2*i+1))
    subplotnum=int(str(c)+str(c)+str(2*i+1))
    ax=fig.add_subplot(subplotnum)
    #ax.imshow(data.T, aspect='auto')
    im = ax.imshow(data.T, aspect='auto',cmap=get_cmap("hot"),origin="lower" )
    title('pic of fits'+'pol '+str(i+1), fontsize = 10)
    ax.set_xlabel('time (s)', fontsize = 10)
    ax.set_ylabel('channel '+'pol'+str(i+1), fontsize = 10)
    #ax.set_xticklabels([str(round(timepoint,1)) for timepoint in np.arange(startn*samppersubint*tsamp, endn*samppersubint*tsamp, (endn - startn)*samppersubint*tsamp/10) ])
    xticks([round(timepoint,1) for timepoint in np.arange(startn*samppersubint, endn*samppersubint+(endn - startn)*samppersubint/10, (endn - startn)*samppersubint/10) ], [str(round(timepoint,1)) for timepoint in np.arange(startn*samppersubint*tsamp, endn*samppersubint*tsamp+(endn - startn)*samppersubint*tsamp/10, (endn - startn)*samppersubint*tsamp/10) ])
    yticks([round(freqpoint,1) for freqpoint in np.arange(0, endfreq- startfreq+(endfreq - startfreq)/5, (endfreq - startfreq)/5) ], [str(round(freqpoint,0)) for freqpoint in np.arange(fch1+startfreq*df, fch1+endfreq*df+(fch1+endfreq*df - (fch1+startfreq*df))/5, (fch1+endfreq*df - (fch1+startfreq*df))/5)])
    fig.colorbar(im, ax = ax)
    #ax.set_xlim(startn*samppersubint*tsamp, endn*samppersubint*tsamp)
    #ax.set_ylim(fch1+startfreq*obsbw, fch1+endfreq*obsbw)
    #if i < 1 :
    #    title(filename.split('/')[-1])
    
    #subplotnum=int(str(2*c)+'1'+str(2*i+2))
    subplotnum=int(str(c)+str(c)+str(2*i+2))
    ax=fig.add_subplot(subplotnum)
    ax.plot(bandpass)
    title('bandpass of '+'pol'+str(i+1), fontsize = 10)
    ax.set_ylabel('bandpass of '+'pol'+str(i+1), fontsize = 10)
    ax.set_xlabel('channel', fontsize = 10)
    xticks([round(freqpoint,1) for freqpoint in np.arange(0, endfreq- startfreq+(endfreq - startfreq)/5, (endfreq - startfreq)/5) ], [str(round(freqpoint,0)) for freqpoint in np.arange(fch1+startfreq*df, fch1+endfreq*df+(fch1+endfreq*df - (fch1+startfreq*df))/5, (fch1+endfreq*df - (fch1+startfreq*df))/5)])
    #ax.set_xlim(0.,d)
    #ax.set_xlim(fch1+startfreq*obsbw, fch1+endfreq*obsbw)
    #colorbar()
    #plot(data.sum(axis=0))
    #plot(data.sum(axis=1))
    #show()
#xlabel('time (s)')
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

f = open(bandpassfilename, 'w')
f.write('MHz       pol1       pol2\n')
for i in range(d):
    f.write(str(bandpassout[i,:]).strip('[').strip(']').strip()+'\n')
f.close()
#print bandpassout

#endtime=datetime.now()
endtime=dt.datetime.now()
print 'START:',starttime
print 'END:',endtime
print 'DURATION:',(endtime-starttime).seconds,' sec'
