#!/bin/bash

#################################
###### Parameters ###############

OBStime="2018/07/28"   #Set obs.time,e.g. 2017/10/13

ZA=60      # Maximum Za (degree)

#################################


echo "Obs_time = " ${OBStime} 
echo "    RA(hms)  DEC(dms)    Rise_time    Transit_time    Set_time"

COUNT=1
cat radec_input.list | while read NAME ; do

    RAJ=`echo ${NAME} | awk '{print $1}'`
    DECJ=`echo ${NAME} | awk '{print $NF}'`

#echo "${NAME}"

python - ${OBStime} ${RAJ} ${DECJ} ${ZA} <<EOF > temp.dat
#!/usr/bin/env python
import numpy as np
import sys
import ephem

ZAangle = 90.0 - np.float64(sys.argv[4]) 
Tianma=ephem.Observer()
Tianma.lat='31:05:13'
Tianma.lon='120:09:48.1'
Tianma.horizon= str(ZAangle) # =(90deg-Maximum Za)
Tianma.date= sys.argv[1]

src = ephem.FixedBody()
src._ra = sys.argv[2]
src._dec = sys.argv[3]
#print Tianma.date,src._ra,src._dec

src.compute()
trise=Tianma.previous_rising(src)
ttrans=Tianma.next_transit(src)
tset=Tianma.next_setting(src)
print ephem.localtime(trise),ephem.localtime(ttrans),ephem.localtime(tset)

#print src.alt,src.az,'next transit : ',ephem.localtime(ttrans)
EOF

Rise_time=`cat temp.dat | awk '{print $1,$2}'`
Transit_time=`cat temp.dat | awk '{print $3,$4}'`
Set_time=`cat temp.dat | awk '{print $5,$6}'`
echo "${COUNT}   ${RAJ} ${DECJ}  ${Rise_time} ${Transit_time} ${Set_time}"

((COUNT++))
done
rm temp.dat
