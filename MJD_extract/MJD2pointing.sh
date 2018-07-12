#!/bin/bash
################################
# Extract pointing(Ra,Dec,GL,GB) from PSR data
################################
#. ~/.bashrc
rm output.list

FLAG=0
DEC=0

 while [ -n "$1" ]; do        
    case "$1" in
    -dec) DEC=$2;;
    -h) HELP=1;echo "#  HELP :";echo " ";echo "-dec : DEC (dd:mm:ss)";echo "Example :$. filename2pointing.sh -dec 30:00:00";echo " ";;
    esac
    shift
 done

tot=`cat MJD.list | wc -l`

for MJD in `cat MJD.list` ; do
let "FLAG = ${FLAG} + 1"
echo "${FLAG}/${tot}   MJD=${MJD}"
python - ${MJD} ${DEC} ${FLAG} <<EOF >> output.list

import sys
import ephem
import datetime as dt
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy import units as u
from datetime import datetime

Dawodang = ephem.Observer()
Dawodang.lat = '25.652939'
Dawodang.lon = '106.8609444'
Dawodang.horizon ='-18'         # Astronomical twilight uses the value -18 degrees

##############################
#    Input parameters

src = ephem.FixedBody()
src._ra = '00:00:00'
Starttime = float(sys.argv[1])  # read MJD time from fits header
src._dec = str(sys.argv[2])
FLAG = int(sys.argv[3])
Offset_time = 26.2144           # half time(sec) between end and start time, ie. beam centre
Offset_arival_time = 236        # interval arrival time(sec) in one day
##############################

# Transfer Fits header MJD --> UTC time
t_header = Time(Starttime,format='mjd',scale='utc')
tmp_t_header = str(t_header.datetime).split('.')
if tmp_t_header.__len__() == 1:
        tmp_t_header[0] = tmp_t_header[0] + '.000001'
else:
        tmp_t_header[0] = tmp_t_header[0] + '.' + tmp_t_header[1]
Starttime_utc = datetime.strptime(tmp_t_header[0],"%Y-%m-%d %H:%M:%S.%f")
Starttime_BJ = Starttime_utc + dt.timedelta(hours=8)

#Inital_Ra = datetime.strptime(str(src._ra),"%Y-%m-%d %H:%M:%S.%f")
#print 'Fits start_time (UTC) =', Starttime_utc             # start time in header

#Dawodang.date = str(Starttime_utc).split(' ')[0]             # Dawodang time = 00:00:00
Dawodang.date = str(Starttime_utc)


# Calculate transit time
src.compute()
ttrans=Dawodang.next_transit(src)
t_transit = Time(ephem.localtime(ttrans),scale='utc')         # localtime UTC+8h
#print ephem.localtime(ttrans), t_transit.mjd                 # localtime UTC+8h, transit time (MJD)
Alt = str(src.alt).split(':')
Az = str(src.az).split(':')
FAST_az = 90.0 - (float(Alt[0])+(float(Alt[1])/60)+float(Alt[2])/3600.)
FAST_el = 270.0 - (float(Az[0])+(float(Az[1])/60)+float(Az[2])/3600.)
#print 'Ra(0:0:0) Transit:', ephem.localtime(ttrans), t_transit.mjd, src.ra, src.dec, src.alt, src.az, FAST_el, FAST_az
tmp=str(t_transit).split('.')
if tmp.__len__()==1:
        tmp[0]=tmp[0]+'.000001'
else:
        tmp[0]=tmp[0]+'.'+tmp[1]

#Transit_utc8 = datetime.strptime(str(t_transit),"%Y-%m-%d %H:%M:%S")
Transit_utc8 = datetime.strptime(tmp[0],"%Y-%m-%d %H:%M:%S.%f")

# Compensate start time & transit time
Delta = Transit_utc8 - Starttime_utc
Offset_sec = 236 * float(Delta.seconds)/24./3600. - float(Offset_time)   # compensate periodical delay and modify start_time to beam centre 

Delta_final = Delta + dt.timedelta(seconds = Offset_sec)

H24_date = (str(Starttime_utc).split(' ')[0]).split('-')
H24 = dt.datetime(int(H24_date[0]), int(H24_date[1]), int(H24_date[2]), 23, 59, 59)
RaJ = H24 - (Delta_final - dt.timedelta(seconds = 3600*8+1))

# Ra,Dec
RaJ_h = (str(RaJ).split(' ')[1]).split(':')[0]
RaJ_m = (str(RaJ).split(' ')[1]).split(':')[1]
RaJ_s = (str(RaJ).split(' ')[1]).split(':')[2]
RaJ_hms = str(RaJ_h)+'h'+str(RaJ_m)+'m'+str(RaJ_s)+'s'
DecJ_d = str(src._dec).split(':')[0]
DecJ_m = str(src._dec).split(':')[1]
DecJ_s = str(src._dec).split(':')[2]
DecJ_dms = str(DecJ_d)+'d'+str(DecJ_m)+'m'+str(DecJ_s)+'s'
RaJ_deg = (str(SkyCoord(RaJ_hms, DecJ_dms, frame='icrs')).split('(')[3]).split(',')[0]

Dec_flag = DecJ_d.find('-')
if (int(Dec_flag) == 0 ):
	DecJ_deg = float(DecJ_d)-float(DecJ_m)/60.-float(DecJ_s)/3600.
else:
	DecJ_deg = float(DecJ_d)+float(DecJ_m)/60.+float(DecJ_s)/3600.

# GL,GB
Glb = SkyCoord(ra=float(RaJ_deg)*u.degree, dec=float(DecJ_deg)*u.degree, frame='icrs')
GL = Glb.galactic.l.degree
GB = Glb.galactic.b.degree
GL = round(float(GL),2)
GB = round(float(GB),2)

print '\n', FLAG
print 'Fits start_time (BJ)  =', Starttime_BJ
print 'Ra(J2000) =', RaJ, '  Ra(deg) =', RaJ_deg
print 'Dec(J2000) =', str(src._dec), '  Dec(deg) =', DecJ_deg
print 'GL(deg) =', GL, '   GB(deg) =', GB

EOF
done
