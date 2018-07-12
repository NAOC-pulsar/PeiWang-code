
import numpy as np
import pyfits

from FastFitsTools.FitsTools import TimeCal


class Fits:
    def __init__(self, filename):
        hdulist=pyfits.open(filename)
        self.telecope = hdulist[0].header['TELESCOP']
        if self.telecope == 'FAST':
            self.hdu0 = hdulist[0]
            self.data1 = hdulist[1].data
            self.header1 = hdulist[1].header

            # number of channel
            self.nchan = hdulist[0].header['OBSNCHAN']
            # time of spera
            self.nsblk = self.header1['NSBLK']
            
            self.initalFreq = self.data1['DAT_FREQ'][0][0]
            self.finalFreq = self.data1['DAT_FREQ'][0][np.size(self.data1['DAT_FREQ'][0]) - 1]

            self.float_tsubint_a = np.array(self.data1['TSUBINT'])
            self.float_offs_sub_a = np.array(self.data1['OFFS_SUB'])
            self.float_lst_sub_a = np.array(self.data1['LST_SUB'])
            self.float_ra_sub_a = np.array(self.data1['RA_SUB'])
            self.float_dec_sub_a = np.array(self.data1['DEC_SUB'])
            self.float_glon_sub_a = np.array(self.data1['GLON_SUB'])
            self.float_glat_sub_a = np.array(self.data1['GLAT_SUB'])
            self.float_fd_ang_a = np.array(self.data1['FD_ANG'])
            self.float_pos_ang_a = np.array(self.data1['POS_ANG'])
            self.float_par_ang_a = np.array(self.data1['PAR_ANG'])
            self.float_tel_az_a = np.array(self.data1['TEL_AZ'])
            self.float_tel_zen_a = np.array(self.data1['TEL_ZEN'])
            self.float_dat_freq_a = self.data1['DAT_FREQ']
            self.float_dat_wts_a = self.data1['DAT_WTS']
            self.float_dat_offs_a = self.data1['DAT_OFFS']
            self.float_dat_scl_a = self.data1['DAT_SCL']
            # Number of rows in table (NSUBINT)
            self.nsubint = int(self.header1['NAXIS2'])
            # totalTime(s)
            self.timePerSubint = self.float_tsubint_a[0]
            # Sample time (s)
            self.sampleTime = self.header1['TBIN']
            # Nr of polarisations
            self.Npolae = self.header1['NPOL']

            self.totalTime = self.timePerSubint * self.nsubint
            self.chanBW = self.header1['CHAN_BW']
            self.centerFreq=self.hdu0.header['OBSFREQ']

            # channel bandwidth

            self.obsbw = self.hdu0.header['OBSBW']

           # self.chnum = self.hdu0.header['OBSNCHAN']

            self.stt_imjd = self.hdu0.header['STT_IMJD']
            self.stt_smjd = self.hdu0.header['STT_SMJD']
            self.stt_offs = self.hdu0.header['STT_OFFS']
            self.nsuboffs = self.header1['NSUBOFFS']
            self.float_data = np.array(self.data1['DATA'])
        if (self.telecope == 'PARKES'):
            self.hdu0 = hdulist[0]

            self.header1 = hdulist[1].header
            self.data1 = hdulist[1].data

            self.header3 = hdulist[3].header
            self.data3 = hdulist[3].data
            # self.initaltime=initaltime
            # self.finaltime=finaltime

            self.nchan = self.data1['NCHAN'][0]

            self.nsblk = self.header3['NSBLK']
            self.finalFreq = self.data3['DAT_FREQ'][0][0]
            self.initalFreq = self.data3['DAT_FREQ'][0][np.size(self.data3['DAT_FREQ'][0]) - 1]
            # print self.initalFreq,self.finalFreq
            self.float_indexval_a = np.array(self.data3['INDEXVAL'])
            self.float_tsubint_a = np.array(self.data3['TSUBINT'])
            self.float_offs_sub_a = np.array(self.data3['OFFS_SUB'])
            self.float_lst_sub_a = np.array(self.data3['LST_SUB'])
            self.float_ra_sub_a = np.array(self.data3['RA_SUB'])
            self.float_dec_sub_a = np.array(self.data3['DEC_SUB'])
            self.float_glon_sub_a = np.array(self.data3['GLON_SUB'])
            self.float_glat_sub_a = np.array(self.data3['GLAT_SUB'])
            self.float_fd_ang_a = np.array(self.data3['FD_ANG'])
            self.float_pos_ang_a = np.array(self.data3['POS_ANG'])
            self.float_par_ang_a = np.array(self.data3['PAR_ANG'])
            self.float_tel_az_a = np.array(self.data3['TEL_AZ'])
            self.float_tel_zen_a = np.array(self.data3['TEL_ZEN'])
            self.float_aux_dm_a = np.array(self.data3['AUX_DM'])
            self.float_aux_rm_a = np.array(self.data3['AUX_RM'])
            self.float_dat_freq_a = self.data3['DAT_FREQ']

            self.float_dat_wts_a = self.data3['DAT_WTS']

            self.float_dat_offs_a = self.data3['DAT_OFFS']

            self.float_dat_scl_a = self.data3['DAT_SCL']

            # Number of rows in table (NSUBINT)
            self.nsubint = int(self.data1['NSUB'])
            # totalTime(s)
            self.timePerSubint = self.float_tsubint_a[0]
            # Sample time (s)
            self.sampleTime = self.header3['TBIN']
            # Nr of polarisations
            self.Npolae = self.data1['NPOL']

            self.totalTime = self.timePerSubint * self.nsubint
            self.chanBW = float(abs(self.data1['CHAN_BW']))


    def modifyPHeader(self,dec):
        #self.fits.chnum = int(endfreqNetNum - startfreqNetNum)
        if (self.telecope == 'FAST'):
            self.hdu0.header['OBSFREQ'] = self.centerFreq

            # channel bandwidth

            self.hdu0.header['OBSBW'] = self.obsbw

            self.hdu0.header['OBSNCHAN'] = self.nchan

            #self.fits.stt_imjd = self.fits.hdu0.header['STT_IMJD']
            #self.fits.stt_smjd = self.fits.hdu0.header['STT_SMJD']
            #self.fits.stt_offs = self.fits.hdu0.header['STT_OFFS']
            #self.fits.nsuboffs = self.fits.header1['NSUBOFFS']
            #print self.fits.stt_imjd, self.fits.stt_smjd, self.fits.stt_offs, self.fits.nsuboffs_a
            mjd = np.float64(
                self.stt_imjd + (np.float64(self.stt_smjd) + np.float64(self.stt_offs)) / np.float64(
                    86400) + self.timePerSubint * self.nsuboffs_a / 86400)

            obj = TimeCal.TimeCal(dec, self.totalTime / 2.)
            res = obj.calTime(mjd)
            ra = res[0]
            FAST_az = res[1]
            FAST_el = res[2]
            RaJ_deg = res[3]

            self.DecJ_deg = res[4]
            self.hdu0.header['SRC_NAME'] = 'NONE'
            self.hdu0.header['RA'] = ra
            self.hdu0.header['DEC'] = dec
            self.float_tel_az_a += FAST_az
            self.float_tel_zen_a += FAST_el
            # self.fits.hdu0.header['STT_CRD1']=
            # self.fits.hdu0.header['STT_CRD2']
            self.hdu0.header['TRK_MODE'] = 'NONE'

        if (self.telecope == 'PARKES'):
            #self.fits.chnum = int(endfreqNetNum - startfreqNetNum)

            self.hdu0.header['OBSFREQ'] = self.fits.centerFreq

        # channel bandwidth
        # print self.fits.chnum , self.fits.chanBW
            self.hdu0.header['OBSBW'] = self.obsbw

            self.hdu0.header['OBSNCHAN'] = self.fits.chnum



        # self.fits.data1['NSUB']=
