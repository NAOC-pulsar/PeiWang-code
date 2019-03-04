#!/bin/bash

Downsamp=1

line=1
cat filelist.txt | while read LINENAME; do
    NUM=`cat filelist.txt | wc -l`
    echo "${line}/${NUM}  ${Filename}"
    Filename=`echo ${LINENAME} | awk '{print $1}'`
    python Downsamp_FASTpsrfits_freq_time_splitpol.py 1024 3071 0 255 ${Downsamp} ${Filename} # for FAST 19beams format (Freq:1.05-1.45GHz)
#   python Downsamp_FASTpsrfits_freq_time_splitpol.py 1160 3207 0 62 ${Downsamp} ${Filename}  # for FAST Ultra-wide band receiver format (Freq:290-802MHz)
    ((line++))
done
