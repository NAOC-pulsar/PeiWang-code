#!/bin/bash

#Rise, Transit, and Set time at FAST Observatory (UTC+8)
#Set obs.time,e.g. 2017/05/21

#===============================


OBStime="2018/01/22"


Horizon="26.4"    # Maximum Za (degree)


#===============================

echo "Obs_time = " ${OBStime} 
echo "    RA(J2000)  DEC(J2000)    FAST_az  FAST_el       RA(Now)    DEC(Now)     	Rise_time          transit_time                     Set_time"

COUNT=1
cat radec_input.list | while read NAME ; do

    RAJ=`echo ${NAME} | awk '{print $1}'`
    DECJ=`echo ${NAME} | awk '{print $NF}'`

#echo "${NAME}"

python - ${OBStime} ${RAJ} ${DECJ} ${Horizon} <<EOF > temp.dat
#!/usr/bin/env python
import numpy as np
import sys
import ephem

ZAangle = 90.0 - np.float64(sys.argv[4])
Dawodang=ephem.Observer()
Dawodang.lat='25.652939'
Dawodang.lon='106.856594'
Dawodang.horizon= str(ZAangle) # =(90deg-Maximum Za)
Dawodang.date= sys.argv[1]

src = ephem.FixedBody()
src._ra = sys.argv[2]
src._dec = sys.argv[3]
#print Dawodang.date,src._ra,src._dec,src.ra,src.dec

src.compute()
trise=Dawodang.previous_rising(src)
ttrans=Dawodang.next_transit(src)
tset=Dawodang.next_setting(src)
print ephem.localtime(trise), ephem.localtime(ttrans), ephem.localtime(tset), src.ra, src.dec, src.alt, src.az

#print src.alt,src.az,'next transit : ',ephem.localtime(ttrans)
EOF
    
Next_transit=`cat temp.dat | awk '{print $7,$8"\t"$1,$2"\t"$3,$4"\t"$5,$6}'`
az=`cat temp.dat | awk '{print $9}'`
Hour_az=`echo "${az}" | sed 's/\:/ /' | awk '{print $1}'`
Min_az=`echo "${az}" | sed 's/\:/ /' | awk '{print $2}' | sed 's/\:/ /'| awk '{print $1}'`
Sec_az=`echo "${az}" | sed 's/\:/ /' | awk '{print $2}' | sed 's/\:/ /'| awk '{print $2}'`
FAST_az=`echo "scale=6; 90-(${Hour_az}+(${Min_az}/60.)+${Sec_az}/3600.)" | bc`

el=`cat temp.dat | awk '{print $10}'`
Hour_el=`echo "${el}" | sed 's/\:/ /' | awk '{print $1}'`
Min_el=`echo "${el}" | sed 's/\:/ /' | awk '{print $2}' | sed 's/\:/ /'| awk '{print $1}'`
Sec_el=`echo "${el}" | sed 's/\:/ /' | awk '{print $2}' | sed 's/\:/ /'| awk '{print $2}'`
DEG_el=`echo "scale=6; ${Hour_el}+(${Min_el}/60)+(${Sec_el}/3600)" | bc`
FAST_el=`echo "scale=6; 270.0-${DEG_el}" | bc`

echo "${COUNT}   ${RAJ} ${DECJ}  ${FAST_el}  ${FAST_az}    ${Next_transit}"
#echo ${Next_transit}

((COUNT++))
done
rm temp.dat
