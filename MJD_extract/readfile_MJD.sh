#!/bin/bash
################################
# Recorded MJD list for PSR data
################################

FLAG=0

for DATASF in `cat SGP.list` ; do  # loop
	let "FLAG = ${FLAG} + 1"
	MJD=`readfile /home/data/psr/201708/13/${DATASF} | grep STT | awk '{print $6}'`
	echo "${FLAG}   ${DATASF}   MJD=${MJD}"
	echo "${MJD}" >> MJD.list
done
