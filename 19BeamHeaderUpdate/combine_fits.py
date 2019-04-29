import numpy as np 
import pyfits
import fitsio
import os
import datetime
import time
import sys
from array import array
import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import *

##############################################################
# 20161008 adapted from cut_FASTpsrfits_freq_time_splitpol.py
#          output 2 pol and pol averaged data
# 20161009 dimension of DAT_OFFS changed from chnum*2 to chnum
#          format of DAT_OFFS changed from dataformat3 to dataformat2
#          size(float_data)/nline/nchan/npol=nsblk
##############################################################

if (len(sys.argv)<3):
  print 'too few inputs!'
  print 'example:'
  print 'python combine_fits.py root fitslist.txt'
  sys.exit()
else:
  print 'input seems OK'

print 'record start time:'
starttime=datetime.datetime.now()
print starttime

fileroot=sys.argv[1]
Fitslist=sys.argv[2]

#u19700101=62135683200.0

#==============================================================
print 'go through the list to get a total row number'
linenum=0
nfile=0
for line in open(Fitslist):
    line1=" ".join(line.split())
#    line1=" ".join(line)
    filename=line1.replace('\n','').split(" ")[0].strip()
    hdulist=fitsio.FITS(filename)

    hdu0 = hdulist[0]
    header0 = hdu0.read_header()

    hdu1 = hdulist[1]
    header1 = hdu1.read_header()

    nchan=header0['OBSNCHAN']
    nline=header1['NAXIS2']
    nsblk=header1['NSBLK']
    linenum=linenum+nline
    nfile=nfile+1


print 'initialize numpy arrays'

#npol=1
#data = np.zeros(linenum,dtype=[('TSUBINT','float64'),('OFFS_SUB','float64'),('LST_SUB','float64'),('RA_SUB','float64'),('DEC_SUB','float64'),('GLON_SUB','float64'),('GLAT_SUB','float64'),('FD_ANG','float32'),('POS_ANG','float32'),('PAR_ANG','float32'),('TEL_AZ','float32'),('TEL_ZEN','float32'),('DAT_FREQ','float32',(nchan)),('DAT_WTS','float32',(nchan)),('DAT_OFFS','float32',(nchan)),('DAT_SCL','float32',(nchan)),('DATA','uint8',(nsblk,npol,nchan,1))])

print 'remove old datafile'
outname=fileroot+'.fits'
rmcomm1='rm -f '+outname
os.system(rmcomm1)
print 'write new datafile'


print 'go through the list to add data to the arrays defined above'
ilinenum=0
ifile=1

reftime=0.0
for line in open(Fitslist):
    print 'Progress: ',ifile,'/',nfile
    line1=" ".join(line.split())
    filename=line1.replace('\n','').split(" ")[0].strip()
    hdulist=fitsio.FITS(filename)

    hdu0 = hdulist[0]
    header0 = hdu0.read_header()

    hdu1 = hdulist[1]
    header1 = hdu1.read_header()

    hdrver=header0['HDRVER']
    date=header0['DATE']
    ant_x=header0['ANT_X']
    ant_y=header0['ANT_Y']
    ant_z=header0['ANT_Z']
    obsfreq=header0['OBSFREQ']
    obsbw=header0['OBSBW']
    nchan=header0['OBSNCHAN']
    ra=header0['RA']
    dec=header0['DEC']
    bmaj=header0['BMAJ']
    bmin=header0['BMIN']
    date_obs=header0['DATE-OBS']
    stt_imjd=header0['STT_IMJD']
    stt_smjd=header0['STT_SMJD']
    stt_offs=header0['STT_OFFS']
    stt_lst=header0['STT_LST']
    nsuboffs=header1['NSUBOFFS']
    nsuboffs=0     # set for DSPSR, 181012
    nchnoffs=header1['NCHNOFFS']
    nsblk=header1['NSBLK']
    npol=header1['NPOL']
    tbin=header1['TBIN']
    chan_bw=header1['CHAN_BW']
    print 'NSBLK: ',nsblk,'sample time(s): ',tbin,'channel width(MHz): ',chan_bw

    nline=header1['NAXIS2']
    pol_type=header1['POL_TYPE']
    

    data=hdulist[1][:]

    if(ifile==1):

#       reftime=(stt_imjd+stt_smjd+stt_offs)*24.0*3600
       reftime=stt_smjd+stt_offs
#       reftime=stt_imjd/86400.+stt_smjd+stt_offs
       print 'first patch of data'
       fitsout=fitsio.FITS(outname,'rw')
       #fitsout.write(data,header=header0)
       fitsout.write(data)
       fitsout[0].write_key('HDRVER',hdrver,comment="")
       fitsout[0].write_key('FITSTYPE','PSRFITS',comment="FITS definition ")
       fitsout[0].write_key('DATE',date,comment="")
       fitsout[0].write_key('OBSERVER','FAST_TEAM',comment="Observer name")
       fitsout[0].write_key('PROJID','Drift',comment="Project name")
       fitsout[0].write_key('TELESCOP','FAST',comment="Telescope name")
       fitsout[0].write_key('ANT_X',ant_x,comment="")
       fitsout[0].write_key('ANT_Y',ant_y,comment="")
       fitsout[0].write_key('ANT_Z',ant_z,comment="")
       fitsout[0].write_key('FRONTEND','WIDEBAND',comment="Frontend ID")
       fitsout[0].write_key('NRCVR',1,comment="")
       fitsout[0].write_key('FD_POLN','LIN',comment="LIN or CIRC")
       fitsout[0].write_key('FD_HAND',1,comment="")
       fitsout[0].write_key('FD_SANG',0.,comment="")
       fitsout[0].write_key('FD_XYPH',0.,comment="")
       fitsout[0].write_key('BACKEND','ROACH',comment="Backend ID")
       fitsout[0].write_key('BECONFIG','N/A',comment="")
       fitsout[0].write_key('BE_PHASE',1,comment="")
       fitsout[0].write_key('BE_DCC',0,comment="")
       fitsout[0].write_key('BE_DELAY',0.,comment="")
       fitsout[0].write_key('TCYCLE',0.,comment="")
       fitsout[0].write_key('OBS_MODE','SEARCH',comment="(PSR, CAL, SEARCH)")
       fitsout[0].write_key('DATE-OBS',date_obs,comment="Date of observation")
       fitsout[0].write_key('OBSFREQ',obsfreq,comment="[MHz] Bandfrequency")
       fitsout[0].write_key('OBSBW',obsbw,comment="[MHz] Bandwidth")
       fitsout[0].write_key('OBSNCHAN',nchan,comment="Number of channels")
       fitsout[0].write_key('CHAN_DM',0.,comment="")
       fitsout[0].write_key('SRC_NAME','Drift',comment="Source or scan ID")
       fitsout[0].write_key('COORD_MD','J2000',comment="")
       fitsout[0].write_key('EQUINOX',2000.,comment="")
       fitsout[0].write_key('BITPIX',8,comment="number of bits per data pixel")
       fitsout[0].write_key('RA',ra,comment="")
       fitsout[0].write_key('DEC',dec,comment="")
       fitsout[0].write_key('BMAJ',bmaj,comment="[deg] Beam major axis length")
       fitsout[0].write_key('BMIN',bmin,comment="[deg] Beam minor axis length")
       fitsout[0].write_key('BPA',0.,comment="[deg] Beam position angle")
       fitsout[0].write_key('STT_CRD1','00:00:00.00',comment="")
       fitsout[0].write_key('STT_CRD2','00:00:00.00',comment="")
       fitsout[0].write_key('TRK_MODE','TRACK',comment="")
       fitsout[0].write_key('STP_CRD1','00:00:00.00',comment="")
       fitsout[0].write_key('STP_CRD2','00:00:00.00',comment="")
       fitsout[0].write_key('SCANLEN',0.,comment="")
       fitsout[0].write_key('FD_MODE','FA',comment="")
       fitsout[0].write_key('FA_REQ',0.,comment="")
       fitsout[0].write_key('CAL_MODE','OFF',comment="")
       fitsout[0].write_key('CAL_FREQ',0.,comment="")
       fitsout[0].write_key('CAL_DCYC',0.,comment="")
       fitsout[0].write_key('CAL_PHS',0.,comment="")
       fitsout[0].write_key('STT_IMJD',stt_imjd,comment="Start MJD (UTC days) (J - long integer)")
       fitsout[0].write_key('STT_SMJD',stt_smjd,comment="[s] Start time (sec past UTC 00h) (J)")
       fitsout[0].write_key('STT_OFFS',stt_offs,comment="[s] Start time offset (D)")
       fitsout[0].write_key('STT_LST',stt_lst,comment="[s] Start LST (D)")
       #fitsout[0].write_key('POL_TYPE','AA',comment="Polarisation identifier")
       #fitsout[0].write_key('NBITS',8,comment="Nr of bits/datum ")
       #fitsout[0].write_key('TBIN',tbin,comment="[s] Time per bin or sample")
       #fitsout[0].write_key('NSBLK',nsblk,comment="Samples/row")
       #fitsout[0].write_key('NBIN',1,comment="Nr of bins (PSR/CAL mode; else 1)")
       #fitsout[0].write_key('NCHAN',nchan,comment="Number of channels")
       #fitsout[0].write_key('NPOL',1,comment="Nr of polarisations")
       #fitsout[0].write_key('POL_TYPE',pol_type,comment="Polarisation identifier")

       fitsout[1].write_key('INT_TYPE','TIME',comment="Time axis (TIME, BINPHSPERI, BINLNGASC, etc)")
       fitsout[1].write_key('INT_UNIT','SEC',comment="Unit of time axis (SEC, PHS (0-1),DEG)")
       fitsout[1].write_key('SCALE','FluxDen',comment="")
       fitsout[1].write_key('NPOL',npol,comment="Nr of polarisations")
       fitsout[1].write_key('POL_TYPE',pol_type,comment="Polarisation identifier")
       fitsout[1].write_key('TBIN',tbin,comment="[s] Time per bin or sample")
       fitsout[1].write_key('NBIN',1,comment="")
       fitsout[1].write_key('NBIN_PRD',0,comment="Nr of bins/pulse period (for gated data)")
       fitsout[1].write_key('PHS_OFFS',0.0,comment="Phase offset of bin 0 for gated data")
       fitsout[1].write_key('NBITS',8,comment="Nr of bits/datum ")
       fitsout[1].write_key('NSUBOFFS',nsuboffs,comment="Subint offset ")
       fitsout[1].write_key('NCHNOFFS',nchnoffs,comment="Channel/sub-band offset for split files")
       fitsout[1].write_key('NCHAN',nchan,comment="Number of channels")
       fitsout[1].write_key('CHAN_BW',chan_bw,comment="[MHz] Channel/sub-band width")
       fitsout[1].write_key('NSBLK',nsblk,comment="Samples/row ")
       fitsout[1].write_key('EXTNAME','SUBINT  ',comment="name of this binary table extension")
       fitsout[1].write_key('EXTVER',1,comment="")
    else:
       print ifile,'th patch of data'
       
       offs_sub=data['OFFS_SUB']
       
#       data['OFFS_SUB']=offs_sub+(stt_imjd+stt_smjd+stt_offs)*24.0*3600-reftime
       data['OFFS_SUB']=offs_sub+(stt_smjd+stt_offs)-reftime
#       data['OFFS_SUB']=offs_sub+(stt_imjd/86400.+stt_smjd+stt_offs)-reftime
       fitsout[-1].append(data)


    ilinenum=ilinenum+nline
    ifile=ifile+1
    #==============================================================

fitsout.close()
print '--------------------------------------------'
print '             Finished!                      '

endtime=datetime.datetime.now()
print 'START:',starttime
print 'END:',endtime
duration=endtime-starttime
print 'DURATION:',duration.seconds,' sec'
