#!/bin/bash
. ~/.bashrc

###### NOTES for FAST Timing (FTp smjd_offset) ######
#####################################################
#
# FTplist.txt is the only-one input-file which is xxx.FTp file list.
# The FTp and RAW_fits files must be included in the same folder when code running.
#
# (The cutted Fits files seems lost the smjd_offset(NSUBOFFS) in header1, so use RAW_fits as input safely.)
#
#####################################################

line=1
cat FTplist.txt | while read FNAME; do
	NUM=`cat FTplist.txt | wc -l`

	VAP=`vap -c stt_imjd,stt_smjd,stt_offs ${FNAME} | grep FTp`
    	
	Filename=`echo ${VAP} | awk '{print $1}'`
	Fitsname=`echo ${Filename} | sed "s/\.FTp/ /" | awk '{print $1}'`
    	IMJD=`echo ${VAP} | awk '{print $2}'`
    	SMJD=`echo ${VAP} | awk '{print $3}'`
	OFFS=`echo ${VAP} | awk '{print $4}'`

python - ${Fitsname} <<EOF > temp.dat
#!/usr/bin/env python
import numpy as np 
import pyfits
import sys

name=sys.argv[1]
hdulist = pyfits.open(name)
hdu0 = hdulist[0]
header0 = hdu0.header
hdu1 = hdulist[1]
header1 = hdu1.header

stt_imjd = header0['STT_IMJD']
stt_smjd = header0['STT_SMJD']
stt_offt = header0['STT_OFFS']
Offset = header1['NSUBOFFS']
Sample = header1['NSBLK']
Tbins = header1['TBIN']

# int and reminder number are splited in smjd and offs.

#temp_smjd = stt_smjd+(np.float64(Offset)*np.float64(Sample)*np.float64(Tbins))
#mod_smjd = int(temp_smjd)
#rem_smjd = np.float64(temp_smjd) - mod_smjd 
#mod_offs = stt_offt+rem_smjd
#if (mod_offs > 1):
#	mod_smjd = mod_smjd + int(mod_offs)
#	mod_offs = mod_offs - int(mod_offs)	
#print stt_imjd, mod_smjd, mod_offs, Offset
print stt_imjd, stt_smjd, stt_offt, Offset
EOF

	Fits_imjd=`cat temp.dat | awk '{print $1}'`
	Fmod_smjd=`cat temp.dat | awk '{print $2}'`
	Fits_offs=`cat temp.dat | awk '{print $3}'`
	Offsetsub=`cat temp.dat | awk '{print $4}'`
	echo ""
#	echo "${line}/${NUM}  Offset ${Offsetsub}Subints for ${Filename}"
	echo "${line}/${NUM}  update for ${Filename}"
	echo "FTp input : imjd=${IMJD}  smjd=${SMJD}  offs=${OFFS}"
	echo "Mod output: imjd=${Fits_imjd}  smjd=${Fmod_smjd}  offs=${Fits_offs}"
	echo ""
	psredit -c ext:stt_smjd="${Fmod_smjd}",ext:stt_offs="${Fits_offs}" -m ${FNAME}

	rm temp.dat
    	((line++))
done	
