#!/bin/bash

line=1
cat filelist.txt | while read LINENAME; do
    NUM=`cat filelist.txt | wc -l`
    echo "${line}/${NUM}  ${Filename}"
    Filename=`echo ${LINENAME} | awk '{print $1}'`
    python cut_FASTpsrfits_freq_time_splitpol.py 1160 3207 0 31 ${Filename}

    ((line++))
done
