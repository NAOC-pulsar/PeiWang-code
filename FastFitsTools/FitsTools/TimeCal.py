#!/usr/bin/env python
# coding=utf-8

print '# Usage:  $python FAST_source_RaJ_DecJ.py MJD DecJ'


import sys
import ephem
import datetime as dt
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy import units as u
from datetime import datetime


class TimeCal:
    def __init__(self,_dec,Offset_time):
        self.Dawodang = ephem.Observer()
        self.Dawodang.lat = '25.652939'
        self.Dawodang.lon = '106.8609444'
        self.Dawodang.horizon = '-18'  # Astronomical twilight uses the value -18 degrees

        ##############################
        #    Input parameters

        self.src = ephem.FixedBody()
        self.src._ra = '00:00:00'
        self.src._dec = _dec
        # Starttime = 57911.55059692592593     # read MJD time from fits header

        self.Offset_time = Offset_time  # half time(sec) between end and start time, ie. beam centre
        Offset_arival_time = 236  # interval arrival time(sec) in one day


        ##############################
    # def mjdtolocaltime(self,Starttime):
    #     t_header = Time(Starttime, format='mjd', scale='utc')
    #     Starttime_utc = datetime.strptime(str(t_header.datetime), "%Y-%m-%d %H:%M:%S.%f")
    #     print Starttime_utc  # start time in header


    def calTime(self,Starttime):
        #print Starttime
        t_header = Time(Starttime, format='mjd', scale='utc')

        tmp_t_header = str(t_header.datetime).split('.')
        # print tmp
        if tmp_t_header.__len__() == 1:
            tmp_t_header[0] = tmp_t_header[0] + '.000001'
            # print tmp[0]
        else:
            tmp_t_header[0] = tmp_t_header[0] + '.' + tmp_t_header[1]
        Starttime_utc = datetime.strptime(tmp_t_header[0], "%Y-%m-%d %H:%M:%S.%f")

        # Inital_Ra = datetime.strptime(str(src._ra),"%Y-%m-%d %H:%M:%S.%f")
        #print 'Fits start_time(UTC) =', Starttime_utc  # start time in header
        # Dawodang.date = str(Starttime_utc).split(' ')[0]             # Dawodang time = 00:00:00
        self.Dawodang.date = str(Starttime_utc)

        # Calculate transit time



    # Calculate transit time

        self.src.compute()
        ttrans = self.Dawodang.next_transit(self.src)

        t_transit = Time(ephem.localtime(ttrans), scale='utc')  # localtime UTC+8h
        # print ephem.localtime(ttrans), t_transit.mjd                 # localtime UTC+8h, transit time (MJD)
        Alt = str(self.src.alt).split(':')
        Az = str(self.src.az).split(':')
        FAST_az = 90.0 - (float(Alt[0]) + (float(Alt[1]) / 60) + float(Alt[2]) / 3600.)
        FAST_el = 270.0 - (float(Az[0]) + (float(Az[1]) / 60) + float(Az[2]) / 3600.)
        # print 'Ra(0:0:0) Transit:', ephem.localtime(ttrans), t_transit.mjd, src.ra, src.dec, src.alt, src.az, FAST_el, FAST_az
        #Transit_utc8 = datetime.strptime(str(t_transit), "%Y-%m-%d %H:%M:%S")
        #print t_transit, '@#@'
        tmp=str(t_transit).split('.')
        #print tmp
        if tmp.__len__()==1:
            tmp[0]=tmp[0]+'.000001'
            #print tmp[0]
        else:
            tmp[0]=tmp[0]+'.'+tmp[1]
            #print tmp[0]
        Transit_utc8 = datetime.strptime(tmp[0],"%Y-%m-%d %H:%M:%S.%f")


        # Compensate start time & transit time

        Delta = Transit_utc8 - Starttime_utc
        Offset_sec = 236 * float(Delta.seconds) / 24. / 3600. - float(
            self.Offset_time)  # compensate periodical delay and modify start_time to beam centre
        # print 'Delta time =', Delta
        # print 'Offset_sec =', Offset_sec

        Delta_final = Delta + dt.timedelta(seconds=Offset_sec)
        # print 'Delta time after offset =', Delta_final

        H24_date = (str(Starttime_utc).split(' ')[0]).split('-')
        H24 = dt.datetime(int(H24_date[0]), int(H24_date[1]), int(H24_date[2]), 23, 59, 59)
        RaJ = H24 - (Delta_final - dt.timedelta(seconds=3600 * 8 + 1))
        #print '\n', 'Ra(J2000) =', RaJ

        # Ra,Dec
        RaJ_h = (str(RaJ).split(' ')[1]).split(':')[0]
        RaJ_m = (str(RaJ).split(' ')[1]).split(':')[1]
        RaJ_s = (str(RaJ).split(' ')[1]).split(':')[2]
        RaJ_hms = str(RaJ_h) + 'h' + str(RaJ_m) + 'm' + str(RaJ_s) + 's'
        DecJ_d = str(self.src._dec).split(':')[0]
        DecJ_m = str(self.src._dec).split(':')[1]
        DecJ_s = str(self.src._dec).split(':')[2]
        DecJ_dms = str(DecJ_d) + 'd' + str(DecJ_m) + 'm' + str(DecJ_s) + 's'
        RaJ_deg = (str(SkyCoord(RaJ_hms, DecJ_dms, frame='icrs')).split('(')[3]).split(',')[0]

        Dec_flag = DecJ_d.find('-')
        if (int(Dec_flag) == 0):
            DecJ_deg = float(DecJ_d) - float(DecJ_m) / 60. - float(DecJ_s) / 3600.
        else:
            DecJ_deg = float(DecJ_d) + float(DecJ_m) / 60. + float(DecJ_s) / 3600.

        # GL,GB
        Glb = SkyCoord(ra=float(RaJ_deg) * u.degree, dec=float(DecJ_deg) * u.degree, frame='icrs')

        GL = Glb.galactic.l.degree
        GB = Glb.galactic.b.degree
        GL = round(float(GL), 2)
        GB = round(float(GB), 2)
        if (GB < 0):
            GB = 'm' + str(GB).split('-')[1]
        else:
            GB = 'p' + str(GB)

        #print '\n', 'GL(deg) =', GL, '   GB(deg) =', GB
        #print '-----------------------------------', '\n'

        return str(RaJ).split(' ')[1], FAST_az, FAST_el, RaJ_deg, DecJ_deg,GL,GB,str(Starttime_utc)
# example to use:
#################################
#obj=TimeCal('-01:31:11.387',26.2144)
# print obj.mjdtolocaltime(57903.84104453703704)
#print obj.calTime(57987.57606337037037)


