# import psutil
import os
import pyfits
# import beam_weighting as wg
import sys

import numpy as np

from bak import TimeCal


class FitsMerge:

    def __init__(self, fits1, fits2, flag, accio,tempfdata):
        if (flag == 1 and (fits1.telecope != fits2.telecope)):
            print 'can not merge  fits  from diff telescope'
            sys.exit()

        self.telecope = fits1.telecope
        self.tmp={fits1,fits2,fits1}

       # if self.telecope == 'FAST':


        #if (self.telecope == 'PARKES'):



            # nline=np.size(temp_float_dat_scl)/2/nchan




    def modifyPHeader(self, startfreq, endfreq, startfreqNetNum, endfreqNetNum,dec):
        # print startfreq,endfreq,'--'
        if (self.telecope == 'FAST'):



       # if (self.telecope == 'PARKES'):


    # @profile

    def merge(self):

        self.tmp[3].float_tsubint_a = np.concatenate(
            (np.array(self.tmp[0].data1['TSUBINT']), np.array(self.tmp[1].data1['TSUBINT'])))
        self.tmp[3].float_offs_sub_a = np.concatenate(
            (np.array(self.tmp[0].data1['OFFS_SUB']), np.array(self.tmp[1].data1['OFFS_SUB'])))

        self.tmp[3].float_lst_sub_a = np.concatenate(
            (np.array(self.tmp[0].data1['LST_SUB']), np.array(self.tmp[1].data1['LST_SUB'])))
        self.tmp[3].float_ra_sub_a = np.concatenate(
            (np.array(self.tmp[0].data1['RA_SUB']), np.array(self.tmp[1].data1['RA_SUB'])))
        self.tmp[3].float_dec_sub_a = np.concatenate(
            (np.array(self.tmp[0].data1['DEC_SUB']), np.array(self.tmp[1].data1['DEC_SUB'])))
        self.tmp[3].float_glon_sub_a = np.concatenate(
            (np.array(self.tmp[0].data1['GLON_SUB']), np.array(self.tmp[1].data1['GLON_SUB'])))
        self.tmp[3].float_glat_sub_a = np.concatenate(
            (np.array(self.tmp[0].data1['GLAT_SUB']), np.array(self.tmp[1].data1['GLAT_SUB'])))
        self.tmp[3].float_fd_ang_a = np.concatenate(
            (np.array(self.tmp[0].data1['FD_ANG']), np.array(self.tmp[1].data1['FD_ANG'])))
        self.tmp[3].float_pos_ang_a = np.concatenate(
            (np.array(self.tmp[0].data1['POS_ANG']), np.array(self.tmp[1].data1['POS_ANG'])))
        self.tmp[3].float_par_ang_a = np.concatenate(
            (np.array(self.tmp[0].data1['PAR_ANG']), np.array(self.tmp[1].data1['PAR_ANG'])))
        self.tmp[3].float_tel_az_a = np.concatenate(
            (np.array(self.tmp[0].data1['TEL_AZ']), np.array(self.tmp[1].data1['TEL_AZ'])))
        self.tmp[3].float_tel_zen_a = np.concatenate(
            (np.array(self.tmp[0].data1['TEL_ZEN']), np.array(self.tmp[1].data1['TEL_ZEN'])))

        self.tmp[3].float_dat_freq_a = np.array(self.tmp[0].data1['DAT_FREQ'])

        self.tmp[3].float_dat_wts_a = np.array(self.tmp[0].data1['DAT_WTS'])

        self.tmp[3].float_dat_offs_a = np.concatenate((self.tmp[0].data1['DAT_OFFS'], self.tmp[1].data1['DAT_OFFS']))

        self.tmp[3].float_dat_scl_a = np.concatenate((self.tmp[0].data1['DAT_SCL'], self.tmp[1].data1['DAT_SCL']))

        self.nsubint = int(self.header1['NAXIS2']) + int(self.header1_2['NAXIS2'])
        # totalTime(s)
        self.timePerSubint = self.tmp[3].float_tsubint_a[0]
        # Sample time (s)
        self.sampleTime = self.header1['TBIN']
        # Nr of polarisations
        self.Npolae = self.header1['NPOL']

        self.totalTime = self.timePerSubint * self.nsubint
        self.chanBW = self.header1['CHAN_BW']

        #self.tmp[3].float_data_1 = tempfdata
        #self.tmp[3].float_data_2 = self.tmp[1].data1['DATA']








        #
        #
        # self.float_data=np.concatenate((self.float_data_1,self.float_data_2),axis=3)
        #
        # self.float_dat_freq = np.concatenate((self.float_dat_freq_a_1,self.float_dat_freq_a_2),axis=1)
        #
        # self.float_dat_wts = np.concatenate((self.float_dat_wts_a_1,self.float_dat_wts_a_2),axis=1)
        #
        # self.float_dat_freq = np.concatenate((self.float_dat_freq_a_1,self.float_dat_freq_a_2),axis=1)
        #
        # self.float_dat_wts = np.concatenate((self.float_dat_wts_a_1,self.float_dat_wts_a_2),axis=1)




