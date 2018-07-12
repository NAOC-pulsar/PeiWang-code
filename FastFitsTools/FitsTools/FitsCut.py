# import psutil
import os
# import beam_weighting as wg
import sys

import numpy as np

import Fits
from FastFitsTools.FitsTools import TimeCal
from FastFitsTools.FitsTools.MergrPolo import mergePolae


class Fitscut:
    # @profile
    def __init__(self, fits,startfreq, endfreq, initaltime, finaltime):
        self.fits = fits
        self.startfreq=startfreq
        self.endfreq=endfreq
        self.initaltime=initaltime
        self.finaltime=finaltime


        # print 'chnum : ',self.fits.chnum
        # print 'startfreqNetNum:',startfreqNetNum,' endfreqNetNum: ',endfreqNetNum
        self.fits.spectraPerSubint = self.fits.timePerSubint / self.fits.sampleTime

        self.initalSubint = int(initaltime / self.fits.timePerSubint)
        self.finalSubint = int(finaltime / self.fits.timePerSubint)

        self.intalSubintNet = int(self.initalSubint * self.fits.nsblk)
        self.finalSubintNet = int(self.finalSubint * self.fits.nsblk)

        if self.fits.nsubint < self.finalSubint:
            finalSubint = self.fits.nsubint

        self.fits.numSubint = int(self.finalSubint - self.initalSubint)
        # initalSubint = int(initalSubint)
        self.fits.nline = self.fits.numSubint


        self.fits.nchan = int(self.fits.nchan)

        if (fits.telecope == 'FAST'):
            self.startfreqNetNum = int((self.startfreq - (self.fits.initalFreq - self.fits.chanBW / 2)) * (1. / self.fits.chanBW))

            self.endfreqNetNum = int((endfreq - (self.fits.initalFreq - self.fits.chanBW / 2)) * (1. / self.fits.chanBW))

        if (fits.telecope == 'PARKES'):
            self.startfreqNetNum = int(((self.fits.finalFreq + self.fits.chanBW / 2) - self.endfreq) * (1. / self.fits.chanBW))

            self.endfreqNetNum = int(((self.fits.finalFreq + self.fits.chanBW / 2) - self.startfreq) * (1. / self.fits.chanBW))

    def checkInputs(self):
        if (self.initaltime < 0 or self.finaltime > self.fits.totalTime or self.initaltime > self.finaltime):
            print 'time inputs error!'
            sys.exit()
        if (self.startfreq < float(self.fits.initalFreq - self.fits.chanBW / 2) or self.endfreq > (
                    self.fits.finalFreq + self.fits.chanBW / 2) or self.startfreq > self.endfreq):
            print self.startfreq, self.endfreq, self.fits.initalFreq, self.fits.finalFreq
            print 'freq inputs error!'
            sys.exit()

    def modifyPHeader(self,dec):
        # print startfreq,endfreq,'--'
        #if (self.fits.telecope == 'FAST'):
        self.fits.nchan = int(self.endfreqNetNum - self.startfreqNetNum)

        self.fits.hdu0.header['OBSFREQ'] = self.fits.centerFreq

        # channel bandwidth

        self.fits.obsbw = self.fits.chnum * self.fits.chanBW
        self.fits.modifyPHeader(dec)
        #self.fits.nchan = self.fits.chnum

        #self.fits.stt_imjd=self.fits.hdu0.header['STT_IMJD']
        #self.fits.stt_smjd=self.fits.hdu0.header['STT_SMJD']
        #self.fits.stt_offs=self.fits.hdu0.header['STT_OFFS']
        #self.fits.nsuboffs = self.fits.header1['NSUBOFFS']


        # print self.fits.stt_imjd,self.fits.stt_smjd,self.fits.stt_offs,self.fits.nsuboffs_a
        #     mjd=np.float64(self.fits.stt_imjd + (np.float64(self.fits.stt_smjd) + np.float64(self.fits.stt_offs)) / np.float64(86400) + self.fits.timePerSubint * self.fits.nsuboffs_a / 86400)
        #
        #     obj = TimeCal.TimeCal(dec, self.fits.totalTime / 4)
        #     res=obj.calTime(mjd)
        #     ra=res[0]
        #     FAST_az=res[1]
        #     FAST_el=res[2]
        #     RaJ_deg=res[3]
        #
        #     self.fits.DecJ_deg=res[4]
        #     self.fits.hdu0.header['SRC_NAME']='NONE'
        #     self.fits.hdu0.header['RA']=ra
        #     self.fits.hdu0.header['DEC']=dec
        #     self.fits.float_tel_az+=FAST_az
        #     self.fits.float_tel_zen+=FAST_el
        #     #self.fits.hdu0.header['STT_CRD1']=
        #     #self.fits.hdu0.header['STT_CRD2']
        #     self.fits.hdu0.header['TRK_MODE']='NONE'
        #
        #
        # if (self.fits.telecope == 'PARKES'):
        #     self.fits.chnum = int(endfreqNetNum - startfreqNetNum)
        #
        #     self.fits.hdu0.header['OBSFREQ'] = self.fits.centerFreq
        #
        #     # channel bandwidth
        #     # print self.fits.chnum , self.fits.chanBW
        #     self.fits.hdu0.header['OBSBW'] = float(self.fits.chnum * self.fits.chanBW)
        #
        #     self.fits.hdu0.header['OBSNCHAN'] = self.fits.chnum



            # self.fits.data1['NSUB']=

            # self.fits.data1['CTR_FREQ']= self.fits.centerFreq
            # self.fits.data1['NCHAN']= self.fits.chnum
            # self.fits.data1['CHAN_BW']

    # @profile

    def cut(self,dec):
        mergePolae(self.fits)
        self.fits.chnum = self.endfreqNetNum - self.startfreqNetNum
        if (self.fits.telecope == "PARKES"):
            self.fits.float_indexval = self.fits.float_indexval_a[self.initalSubint:self.finalSubint]
            self.fits.float_aux_dm = self.fits.float_aux_dm_a[self.initalSubint:self.finalSubint]
            self.fits.float_aux_rm = self.fits.float_aux_rm_a[self.initalSubint:self.finalSubint]

        self.fits.float_tsubint = self.fits.float_tsubint_a[self.initalSubint:self.finalSubint]

        self.fits.float_offs_sub = self.fits.float_offs_sub_a[self.initalSubint:self.finalSubint]

        self.fits.float_lst_sub = self.fits.float_lst_sub_a[self.initalSubint:self.finalSubint]

        self.fits.float_ra_sub = self.fits.float_ra_sub_a[self.initalSubint:self.finalSubint]

        self.fits.float_dec_sub = self.fits.float_dec_sub_a[self.initalSubint:self.finalSubint]

        self.fits.float_glon_sub = self.fits.float_glon_sub_a[self.initalSubint:self.finalSubint]

        self.fits.float_glat_sub = self.fits.float_glat_sub_a[self.initalSubint:self.finalSubint]

        self.fits.float_fd_ang = self.fits.float_fd_ang_a[self.initalSubint:self.finalSubint]

        self.fits.float_pos_ang = self.fits.float_pos_ang_a[self.initalSubint:self.finalSubint]

        self.fits.float_par_ang = self.fits.float_par_ang_a[self.initalSubint:self.finalSubint]

        self.fits.float_tel_az = self.fits.float_tel_az_a[self.initalSubint:self.finalSubint]

        self.fits.float_tel_zen = self.fits.float_tel_zen_a[self.initalSubint:self.finalSubint]

        self.fits.float_dat_freq = np.zeros([self.fits.nline, int(self.endfreqNetNum - self.startfreqNetNum)])

        self.fits.float_dat_wts = np.zeros([self.fits.nline, int(self.endfreqNetNum - self.startfreqNetNum)])

        self.fits.float_dat_freq = np.array(self.fits.float_dat_freq_a)[self.initalSubint:self.finalSubint, self.startfreqNetNum:self.endfreqNetNum]

        self.fits.float_dat_wts = np.array(self.fits.float_dat_wts_a)[self.initalSubint:self.finalSubint, self.startfreqNetNum:self.endfreqNetNum]
        self.fits.nsuboffs_a=(self.fits.float_offs_sub[0]-0.5*self.fits.timePerSubint)/self.fits.timePerSubint+1e-7
        # print 'chnum:',self.fits.chnum,startfreqNetNum,endfreqNetNum,self.fits.nchan,self.fits.float_dat_offs.shape
        if (self.fits.telecope == 'FAST'):
            self.fits.float_dat_offs = np.zeros([self.fits.nline, self.fits.chnum * 2])

            self.fits.float_dat_scl = np.zeros([self.fits.nline, self.fits.chnum * 2])

            self.fits.float_dat_offs[:, 0:self.fits.chnum] = np.array(self.fits.float_dat_offs_a)[self.initalSubint:self.finalSubint,
                                                             self.startfreqNetNum:self.endfreqNetNum]
            # print np.array(self.fits.data1['DAT_OFFS'])[self.initalSubint:self.finalSubint,(startfreqNetNum+self.fits.nchan):endfreqNetNum+1+self.fits.nchan].shape,(startfreqNetNum+self.fits.nchan),(endfreqNetNum+1+self.fits.nchan)
            self.fits.float_dat_offs[:, self.fits.chnum:2 * self.fits.chnum] = np.array(self.fits.float_dat_offs_a)[
                                                                self.initalSubint:self.finalSubint,
                                                                               self.startfreqNetNum + self.fits.nchan:self.endfreqNetNum + self.fits.nchan]

            self.fits.float_dat_scl[:, 0:self.fits.chnum] = np.array(self.fits.float_dat_scl_a)[self.initalSubint:self.finalSubint,
                                                            self.startfreqNetNum:self.endfreqNetNum]

            self.fits.float_dat_scl[:, self.fits.chnum:2 * self.fits.chnum] = np.array(self.fits.float_dat_scl_a)[self.initalSubint:self.finalSubint,
                                                                              self.startfreqNetNum + self.fits.nchan:self.endfreqNetNum + self.fits.nchan]
            # self.fits.float_data = np.array(self.fits.data1['DATA'])
        if (self.fits.telecope == 'PARKES'):
            self.fits.float_dat_offs = np.zeros([self.fits.nline, self.fits.chnum])

            self.fits.float_dat_scl = np.zeros([self.fits.nline, self.fits.chnum])
            self.fits.float_dat_offs[:, 0:self.fits.chnum] = np.array(self.fits.float_dat_offs_a)[self.initalSubint:self.finalSubint,
                                                             self.startfreqNetNum:self.endfreqNetNum]
            # print np.array(self.fits.data1['DAT_OFFS'])[self.initalSubint:self.finalSubint,(startfreqNetNum+self.fits.nchan):endfreqNetNum+1+self.fits.nchan].shape,(startfreqNetNum+self.fits.nchan),(endfreqNetNum+1+self.fits.nchan)


            self.fits.float_dat_scl[:, 0:self.fits.chnum] = np.array(self.fits.float_dat_scl_a)[self.initalSubint:self.finalSubint,
                                                            self.startfreqNetNum:self.endfreqNetNum]
            self.fits.float_data = np.array(self.fits.data3['DATA'])

            # self.fits.float_data2= (self.fits.float_data.reshape(self.fits.nsubint*self.fits.nsblk, self.fits.nchan)[intalSubintNet:finalSubintNet, startfreqNetNum: endfreqNetNum])\
            #   .reshape(self.fits.nline,self.fits.nsblk,1,self.fits.chnum)

        if (self.fits.telecope == 'FAST'):
            self.fits.float_data2 = (

                (self.fits.float_data.reshape(self.fits.nsubint * self.fits.nsblk, self.fits.nchan))[self.intalSubintNet:self.finalSubintNet,
                self.startfreqNetNum: self.endfreqNetNum]) \
                .reshape(self.fits.nline, self.fits.nsblk, 1, self.fits.chnum,1)
            self.modifyPHeader(dec)
            #self.fits.float_data2 = np.zeros([self.fits.nline, self.fits.nsblk, 1, self.fits.chnum,1])
            #self.fits.float_data2+=258
        if (self.fits.telecope == 'PARKES'):
            self.fits.float_data2 = (

                self.fits.float_data.reshape(self.fits.nsubint * self.fits.nsblk, self.fits.nchan)[self.intalSubintNet:self.finalSubintNet,
                self.startfreqNetNum: self.endfreqNetNum]) \
                .reshape(self.fits.nline, self.fits.nsblk * 1 * self.fits.chnum * 1)

        return self.fits
            # self.fits.float_data2 = np.zeros([self.fits.numSubint, np.size(self.fits.float_data) / self.fits.nsubint / self.fits.nchan * self.fits.chnum])
            # subintRange = range(int(self.fits.nline))
            #
            #
            #
            # for i in [x + initalSubint for x in subintRange]:
            #     # print i,self.fits.float_data.shape,self.fits.nchan
            #     temp_data = self.fits.float_data[i, :].reshape([np.size(self.fits.float_data[i, :]) / self.fits.nchan, self.fits.nchan])
            #     # print temp_data.shape
            #     # print startfreqNetNum,endfreqNetNum,i,self.fits.nchan,self.fits.chnum
            #     temp_data2 = temp_data[:, startfreqNetNum:endfreqNetNum].reshape(
            #         np.size(self.fits.float_data[i, :]) / self.fits.nchan * self.fits.chnum)
            #
            #     self.fits.float_data2[i - initalSubint, :] = temp_data2


    # def exeCutTimeFreq(self, startfreq, endfreq, initaltime, finaltime, i, outpath, interval, mode, outname,
    #                    dec):
    #     self.fits.centerFreq = (startfreq + endfreq - 1) / 2
    #     self.fits.checkInputs(startfreq, endfreq, initaltime, finaltime)
    #     # initaltime = int(round(initaltime / self.fits.timePerSubint)) * self.fits.timePerSubint
    #     # finaltime = int(round(finaltime / self.fits.timePerSubint)) * self.fits.timePerSubint
    #     # print self.fits.telecope
    #     if (self.fits.telecope == 'FAST'):
    #         startfreqNetNum = int((startfreq - (self.fits.initalFreq - self.fits.chanBW / 2)) * (1. / self.fits.chanBW))
    #
    #         endfreqNetNum = int((endfreq - (self.fits.initalFreq - self.fits.chanBW / 2)) * (1. / self.fits.chanBW))
    #
    #     if (self.fits.telecope == 'PARKES'):
    #         startfreqNetNum = int(((self.fits.finalFreq + self.fits.chanBW / 2) - endfreq) * (1. / self.fits.chanBW))
    #
    #         endfreqNetNum = int(((self.fits.finalFreq + self.fits.chanBW / 2) - startfreq) * (1. / self.fits.chanBW))
    #
    #
    #     self.fits.cut(startfreqNetNum, endfreqNetNum, initaltime, finaltime)
    #     self.fits.modifyPHeader(startfreq, endfreq, startfreqNetNum, endfreqNetNum, dec)
