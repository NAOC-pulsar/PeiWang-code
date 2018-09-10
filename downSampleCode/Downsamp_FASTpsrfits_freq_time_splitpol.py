import numpy as np 
import pyfits
import os
import datetime
import time
import sys
from array import array
from pylab import *

##############################################################
# Adapted from Downsamp_FASTpsrfits_freq_time_splitpol.py
# 
# Output data for a selected time & freq. range and frequency downsampling rate in Fits format.
# (Output 2 pols and pols averaged Fits format datafiles)
#
# PeiWang 2018/09/09
##############################################################

if (len(sys.argv)<6 or len(sys.argv)>7):
  	print '\n','Input error!','\n'
  	print '# Example:'
 	print '   python cut_FASTpsrfits.py startchan endchan startn endn xxx.fits'
	print 'or python cut_FASTpsrfits.py startchan endchan startn endn Fdsamp xxx.fits'
	print '(Fdsamp is downsampling rate on frequency channels, unit in 2^n)','\n'
	sys.exit()
elif len(sys.argv) == 6:
	startfreq=int(sys.argv[1])
	endfreq=int(sys.argv[2])
	startn=int(sys.argv[3])
	endn=int(sys.argv[4])
	filename=sys.argv[5]
	Fdsamp=1
elif len(sys.argv) == 7:
	startfreq=int(sys.argv[1])
	endfreq=int(sys.argv[2])
	startn=int(sys.argv[3])
	endn=int(sys.argv[4])
	Fdsamp=int(sys.argv[5])
	filename=sys.argv[6]

starttime=datetime.datetime.now()
linenum=endn-startn+1
chnum=endfreq-startfreq+1

if chnum%Fdsamp != 0:
	print '\n','# Error! The input of "endfreq-startfreq+1" not be divided by "Fdsamp" !','\n'
	sys.exit()

#filename='J0826+2637_tracking_6-M01_0001.fits'
fileroot=filename[0:-5]
print fileroot, ', Downsampling rate =', Fdsamp

#u19700101=62135683200.0

hdulist = pyfits.open(filename)

hdu0 = hdulist[0]
data0 = hdu0.data
header0 = hdu0.header
print data0
hdu1 = hdulist[1]
data1 = hdu1.data
header1 = hdu1.header

float_data=np.array(data1['DATA'])
temp_float_dat_scl=np.array(data1['DAT_SCL'])
nline=header1['NAXIS2']
nsblk=header1['NSBLK']
tbin=header1['TBIN']
npol=header1['NPOL']
chan_bw=header1['CHAN_BW']
freq=header0['OBSFREQ']
nchan=header0['OBSNCHAN']
print 'Input  Number of subints =', size(temp_float_dat_scl)/npol/nchan, nline
print '       Ntsamp each subint=', nsblk, size(float_data)/nline/npol/nchan, size(float_data)/nline/nchan/npol
print '       Central freq(MHz) =', freq
print '       Freq. bandwidth   =', header0['OBSBW']
print '       Channel number    =', nchan
print '       Channel width(MHz)=', chan_bw
print '       data1[\'DATA\']     =', float_data.shape
hdu0.header['OBSFREQ']=((endfreq-startfreq)*1.0/2+1.0 - ((nchan-1.0)*1.0/2+1))*chan_bw + freq
hdu0.header['OBSBW']=chnum*chan_bw*1.0
hdu0.header['OBSNCHAN']=chnum/Fdsamp*1.0
print 'Output Number of subints =', linenum
print '       Ntsamp each subint=', 'Same as input'
print '       Central freq(MHz) =', hdu0.header['OBSFREQ']
print '       Freq. bandwidth   =', hdu0.header['OBSBW']
print '       Channel number    =', hdu0.header['OBSNCHAN']
print '       Channel width(MHz)=', hdu0.header['OBSBW']/hdu0.header['OBSNCHAN'], chan_bw*Fdsamp*1.0

float_tsubint=np.array(data1['TSUBINT'])[startn:endn+1]
float_offs_sub=np.array(data1['OFFS_SUB'])[startn:endn+1]
float_lst_sub=np.array(data1['LST_SUB'])[startn:endn+1]
float_ra_sub=np.array(data1['RA_SUB'])[startn:endn+1]
float_dec_sub=np.array(data1['DEC_SUB'])[startn:endn+1]
float_glon_sub=np.array(data1['GLON_SUB'])[startn:endn+1]
float_glat_sub=np.array(data1['GLAT_SUB'])[startn:endn+1]
float_fd_ang=np.array(data1['FD_ANG'])[startn:endn+1]
float_pos_ang=np.array(data1['POS_ANG'])[startn:endn+1]
float_par_ang=np.array(data1['PAR_ANG'])[startn:endn+1]
float_tel_az=np.array(data1['TEL_AZ'])[startn:endn+1]
float_tel_zen=np.array(data1['TEL_ZEN'])[startn:endn+1]
#float_aux_dm=np.array(data1['AUX_DM'])[startn:endn+1]
#float_aux_rm=np.array(data1['AUX_RM'])[startn:endn+1]

float_dat_freq=np.zeros([linenum, chnum/Fdsamp])
float_dat_wts=np.zeros([linenum, chnum/Fdsamp])
float_dat_offs=np.zeros([linenum, chnum/Fdsamp])
float_dat_scl=np.zeros([linenum, chnum/Fdsamp])

float_dat_freq=np.array(data1['DAT_FREQ'])[startn:endn+1,startfreq:endfreq+1].reshape(linenum,chnum/Fdsamp,Fdsamp).sum(axis=-1)/Fdsamp
float_dat_wts=np.array(data1['DAT_WTS'])[startn:endn+1,startfreq:endfreq+1].reshape(linenum,chnum/Fdsamp,Fdsamp).sum(axis=-1)/Fdsamp
float_dat_offs=np.array(data1['DAT_OFFS'])[startn:endn+1,startfreq:endfreq+1].reshape(linenum,chnum/Fdsamp,Fdsamp).sum(axis=-1)/Fdsamp
float_dat_scl=np.array(data1['DAT_SCL'])[startn:endn+1,startfreq:endfreq+1].reshape(linenum,chnum/Fdsamp,Fdsamp).sum(axis=-1)/Fdsamp

float_data2=np.zeros([linenum,nsblk*chnum/Fdsamp])
#float_data3=np.zeros([linenum,size(float_data)/nline/nchan/npol*chnum/Fdsamp])
float_data3=np.zeros([linenum,nsblk*chnum/Fdsamp])
#float_data_tot=np.zeros([linenum,size(float_data)/nline/nchan/npol*chnum/Fdsamp])
float_data_tot=np.zeros([linenum,nsblk*chnum/Fdsamp])

#dataformat=str(size(float_data2)/linenum/Fdsamp)+'B'
dataformat=str(nsblk*chnum/Fdsamp)+'B'

#print dataformat,(float_data2).shape
for i in range(linenum):
     temp_data=float_data[i+startn,:].reshape([size(float_data[i+startn,:])/nchan/npol,npol*nchan])
#     temp_data2=temp_data[:,startfreq:endfreq+1].reshape(size(float_data[i+startn,:])/nchan/npol*chnum)
     temp_data2=temp_data[:,startfreq:endfreq+1].reshape(size(float_data[i+startn,:])/nchan/npol*chnum/Fdsamp,Fdsamp).sum(axis=-1)/Fdsamp
#     temp_data3=temp_data[:,nchan+startfreq:nchan+endfreq+1].reshape(size(float_data[i+startn,:])/nchan/npol*chnum)
     temp_data3=temp_data[:,nchan+startfreq:nchan+endfreq+1].reshape(size(float_data[i+startn,:])/nchan/npol*chnum/Fdsamp,Fdsamp).sum(axis=-1)/Fdsamp
     temp_data_tot=(temp_data2+temp_data3)/2
     float_data2[i, :]=temp_data2
     float_data3[i, :]=temp_data3
     float_data_tot[i, :]=temp_data_tot

#dataformat=str(size(float_data)/nline/nchan*chnum/Fdsamp)+'E'
dataformat2=str(chnum/Fdsamp)+'E'
#print dataformat,dataformat2,dataformat3

#column1_data = pyfits.Column(name='INDEXVAL',format='1D',array=float_indexval)
column2_data = pyfits.Column(name='TSUBINT',format='1D',array=float_tsubint,unit='s')
column3_data = pyfits.Column(name='OFFS_SUB',format='1D',array=float_offs_sub,unit='s')
column4_data = pyfits.Column(name='LST_SUB',format='1D',array=float_lst_sub,unit='s')
column5_data = pyfits.Column(name='RA_SUB',format='1D',array=float_ra_sub,unit='deg')
column6_data = pyfits.Column(name='DEC_SUB',format='1D',array=float_dec_sub,unit='deg')
column7_data = pyfits.Column(name='GLON_SUB',format='1D',array=float_glon_sub,unit='deg')
column8_data = pyfits.Column(name='GLAT_SUB',format='1D',array=float_glat_sub,unit='deg')
column9_data = pyfits.Column(name='FD_ANG',format='1E',array=float_fd_ang,unit='deg')
column10_data = pyfits.Column(name='POS_ANG',format='1E',array=float_pos_ang,unit='deg')
column11_data = pyfits.Column(name='PAR_ANG',format='1E',array=float_par_ang,unit='deg')
column12_data = pyfits.Column(name='TEL_AZ',format='1E',array=float_tel_az,unit='deg')
column13_data = pyfits.Column(name='TEL_ZEN',format='1E',array=float_tel_zen,unit='deg')
#column14_data = pyfits.Column(name='AUX_DM',format='1E',array=float_aux_dm)
#column15_data = pyfits.Column(name='AUX_RM',format='1E',array=float_aux_rm)
#column16_data = pyfits.Column(name='DAT_FREQ',format=dataformat2,array=float_dat_freq)
column16_data = pyfits.Column(name='DAT_FREQ',format=dataformat2,array=float_dat_freq,unit='deg')
column17_data = pyfits.Column(name='DAT_WTS',format=dataformat2,array=float_dat_wts,unit='deg')
column18_data = pyfits.Column(name='DAT_OFFS',format=dataformat2,array=float_dat_offs,unit='deg') 
column19_data = pyfits.Column(name='DAT_SCL',format=dataformat2,array=float_dat_scl,unit='MHz')

column20_data = pyfits.Column(name='DATA',format=dataformat,array=float_data2,unit='Jy')
column20_data_2 = pyfits.Column(name='DATA',format=dataformat,array=float_data3,unit='Jy')
column20_data_tot = pyfits.Column(name='DATA',format=dataformat,array=float_data_tot,unit='Jy')
print '       Pol 1   float_data2    =', float_data2.shape
print '       Pol 2   float_data3    =', float_data3.shape
print '       Pol_tot float_data_tot =', float_data_tot.shape

table_hdu = pyfits.new_table([column2_data,column3_data,column4_data,column5_data,column6_data,column7_data,column8_data,column9_data,column10_data,column11_data,column12_data,column13_data,column16_data,column17_data,column18_data,column19_data,column20_data])

table_hdu.header.append(('INT_TYPE','TIME','Time axis (TIME, BINPHSPERI, BINLNGASC, etc)'))
table_hdu.header.append(('INT_UNIT','SEC','Unit of time axis (SEC, PHS (0-1),DEG)'))
table_hdu.header.append(('SCALE','FluxDec','Intensiy units (FluxDec/RefFlux/Jansky)'))
table_hdu.header.append(('NPOL',1,'Nr of polarisations'))
table_hdu.header.append(('POL_TYPE','AABB','Polarisation identifier (e.g., AABBCRCI, AA+BB)'))
table_hdu.header.append(('TBIN',tbin,'[s] Time per bin or sample'))
table_hdu.header.append(('NBIN',1,'Nr of bins (PSR/CAL mode; else 1)'))
table_hdu.header.append(('NBIN_PRD',0,'Nr of bins/pulse period (for gated data)'))
table_hdu.header.append(('PHS_OFFS',0.0,'Phase offset of bin 0 for gated data'))
table_hdu.header.append(('NBITS',8,'Nr of bits/datum (SEARCH mode "X" data, else 1)'))
table_hdu.header.append(('NSUBOFFS',0,'Subint offset (Contiguous SEARCH-mode files)'))
table_hdu.header.append(('NCHAN',chnum/Fdsamp,'Number of channels/sub-bands in this file'))
table_hdu.header.append(('CHAN_BW',chan_bw,'[MHz] Channel/sub-band width'))
table_hdu.header.append(('NCHNOFFS',0,'Channel/sub-band offset for split files'))
table_hdu.header.append(('NSBLK',nsblk,'Samples/row (SEARCH mode, else 1)'))
table_hdu.header.append(('EXTNAME','SUBINT  ','name of this binary table extension'))

table_hdu2 = pyfits.new_table([column2_data,column3_data,column4_data,column5_data,column6_data,column7_data,column8_data,column9_data,column10_data,column11_data,column12_data,column13_data,column16_data,column17_data,column18_data,column19_data,column20_data_2])

table_hdu2.header.append(('INT_TYPE','TIME','Time axis (TIME, BINPHSPERI, BINLNGASC, etc)'))
table_hdu2.header.append(('INT_UNIT','SEC','Unit of time axis (SEC, PHS (0-1),DEG)'))
table_hdu2.header.append(('SCALE','FluxDec','Intensiy units (FluxDec/RefFlux/Jansky)'))
table_hdu2.header.append(('NPOL',1,'Nr of polarisations'))
table_hdu2.header.append(('POL_TYPE','AABB','Polarisation identifier (e.g., AABBCRCI, AA+BB)'))
table_hdu2.header.append(('TBIN',tbin,'[s] Time per bin or sample'))
table_hdu2.header.append(('NBIN',1,'Nr of bins (PSR/CAL mode; else 1)'))
table_hdu2.header.append(('NBIN_PRD',0,'Nr of bins/pulse period (for gated data)'))
table_hdu2.header.append(('PHS_OFFS',0.0,'Phase offset of bin 0 for gated data'))
table_hdu2.header.append(('NBITS',8,'Nr of bits/datum (SEARCH mode "X" data, else 1)'))
table_hdu2.header.append(('NSUBOFFS',0,'Subint offset (Contiguous SEARCH-mode files)'))
table_hdu2.header.append(('NCHAN',chnum/Fdsamp,'Number of channels/sub-bands in this file'))
table_hdu2.header.append(('CHAN_BW',chan_bw,'[MHz] Channel/sub-band width'))
table_hdu2.header.append(('NCHNOFFS',0,'Channel/sub-band offset for split files'))
table_hdu2.header.append(('NSBLK',nsblk,'Samples/row (SEARCH mode, else 1)'))
table_hdu2.header.append(('EXTNAME','SUBINT  ','name of this binary table extension'))

table_hdu3 = pyfits.new_table([column2_data,column3_data,column4_data,column5_data,column6_data,column7_data,column8_data,column9_data,column10_data,column11_data,column12_data,column13_data,column16_data,column17_data,column18_data,column19_data,column20_data_tot])

table_hdu3.header.append(('INT_TYPE','TIME','Time axis (TIME, BINPHSPERI, BINLNGASC, etc)'))
table_hdu3.header.append(('INT_UNIT','SEC','Unit of time axis (SEC, PHS (0-1),DEG)'))
table_hdu3.header.append(('SCALE','FluxDec','Intensiy units (FluxDec/RefFlux/Jansky)'))
table_hdu3.header.append(('NPOL',1,'Nr of polarisations'))
table_hdu3.header.append(('POL_TYPE','AABB','Polarisation identifier (e.g., AABBCRCI, AA+BB)'))
table_hdu3.header.append(('TBIN',tbin,'[s] Time per bin or sample'))
table_hdu3.header.append(('NBIN',1,'Nr of bins (PSR/CAL mode; else 1)'))
table_hdu3.header.append(('NBIN_PRD',0,'Nr of bins/pulse period (for gated data)'))
table_hdu3.header.append(('PHS_OFFS',0.0,'Phase offset of bin 0 for gated data'))
table_hdu3.header.append(('NBITS',8,'Nr of bits/datum (SEARCH mode "X" data, else 1)'))
table_hdu3.header.append(('NSUBOFFS',0,'Subint offset (Contiguous SEARCH-mode files)'))
table_hdu3.header.append(('NCHAN',chnum/Fdsamp,'Number of channels/sub-bands in this file'))
table_hdu3.header.append(('CHAN_BW',chan_bw,'[MHz] Channel/sub-band width'))
table_hdu3.header.append(('NCHNOFFS',0,'Channel/sub-band offset for split files'))
table_hdu3.header.append(('NSBLK',nsblk,'Samples/row (SEARCH mode, else 1)'))
table_hdu3.header.append(('EXTNAME','SUBINT  ','name of this binary table extension'))

hdulist2 = pyfits.HDUList([hdu0,table_hdu])
#hdulist2 = pyfits.HDUList([hdu0])
#os.system('rm -f FASTpsrfits_out_pol1.fits')
#hdulist2.writeto('FASTpsrfits_out_pol1.fits')
outname1=fileroot+'_pol1_'+sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[4]+'_Fdsamp'+str(Fdsamp)+'.fits'
rmcomm1='rm -f '+outname1
os.system(rmcomm1)
hdulist2.writeto(outname1)
hdulist3 = pyfits.HDUList([hdu0,table_hdu2])
#os.system('rm -f FASTpsrfits_out_pol2.fits')
#hdulist3.writeto('FASTpsrfits_out_pol2.fits')
outname2=fileroot+'_pol2_'+sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[4]+'_Fdsamp'+str(Fdsamp)+'.fits'
rmcomm2='rm -f '+outname2
os.system(rmcomm2)
hdulist3.writeto(outname2)

hdulist4 = pyfits.HDUList([hdu0,table_hdu3])
#os.system('rm -f FASTpsrfits_out_tot.fits')
#hdulist4.writeto('FASTpsrfits_out_tot.fits')
outname3=fileroot+'_tot_'+sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[4]+'_Fdsamp'+str(Fdsamp)+'.fits'
rmcomm3='rm -f '+outname3
os.system(rmcomm3)
hdulist4.writeto(outname3)

print '--------------------------------------------'
print '             Finished!                      '
endtime=datetime.datetime.now()
print 'START:',starttime
print 'END:',endtime
duration=endtime-starttime
print 'DURATION:',duration.seconds,' sec'
