#!/bin/bash

#Set obs.time,e.g. 2017/05/21
#===============================


OBStime="2018/7/28"


Horizon="75"    # Maximum Za (degree)


#===============================

echo "Obs_time = " ${OBStime} 

echo "PSRJ	RA(hh:mm:ss)	DEC(hh:mm:ss)	RA(deg)  	DEC(deg)     P0(s)	DM	S400(mJy)	S1400(mJy)	S2000(mJy)	Rise_time             transit_time              Set_time" > PSR_transit_time_FAST.list

COUNT=1
for NAME in `cat Jname_input.list` ; do
#NAME="J2129+1210A"

echo "${COUNT} ${NAME}"

    RAJ=`psrcat -c "raj" ${NAME} -x -o short`
    DECJ=`psrcat -c "decj" ${NAME} -x -o short`
    RAJD=`psrcat -c "rajd" ${NAME} -x -o short`
    DECJD=`psrcat -c "decjd" ${NAME} -x -o short`
    P0=`psrcat -c "P0" ${NAME} -x -o short`
    DM=`psrcat -c "DM" ${NAME} -x -o short`
#    W50=`psrcat -c "w50" ${NAME} -x -o short`
#    W10=`psrcat -c "w10" ${NAME} -x -o short`
    S400=`psrcat -c "S400" ${NAME} -x -o short`
    S1400=`psrcat -c "S1400" ${NAME} -x -o short`
    S2000=`psrcat -c "S2000" ${NAME} -x -o short`

    python - ${OBStime} ${RAJ} ${DECJ} ${Horizon} <<EOF > temp.dat

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
print ephem.localtime(trise), ephem.localtime(ttrans), ephem.localtime(tset)
#print src.alt,src.az,'next transit : ',ephem.localtime(ttrans)
EOF
    
Rise=`cat temp.dat | awk '{print $1,$2}'`
Next_transit=`cat temp.dat | awk '{print $3,$4}'`
Set=`cat temp.dat | awk '{print $5,$6}'`
#echo $Next_transit    
echo "${NAME} ${RAJ} ${DECJ} ${RAJD} ${DECJD} ${P0} ${DM} ${S400} ${S1400} ${S2000} ${Rise}     ${Next_transit}     ${Set}" >> PSR_transit_time_FAST.list

((COUNT++))
done
rm temp.dat
