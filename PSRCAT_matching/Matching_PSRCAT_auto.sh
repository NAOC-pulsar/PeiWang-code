#!/bin/bash
# This is a bash script used for matching PSR parameters e.g. P0,DM,RA,DEC... with "PSR_17.08.27.list".
# DataList, PSR_17.08.27.list are input files.

. ~/.bashrc

NUMPSR=2536     # Total number of PSR in input file (PSR_17.08.27.list)

ERRORdeg=0
ERRORp0=0
ERRORdm=0
HARMmax=0
HELP=0
DEF=0

while [ -n "$1" ]; do         # Setting readin parameters for PSR deviated range
      case "$1" in
      -radecd) ERRORdeg=$2;;
      -p0d) ERRORp0=$2;;
      -dmd) ERRORdm=$2;;
      -harm) HARMmax=$2;;
      -h) HELP=1;echo "#  HELP :";echo " ";echo "-radecd : Position deviation in RA and DEC (degree)";echo "-p0d    : Period deviation in p0 (ms)";echo "-dmd    : Dispertion measure deviation in (pc * cm^-3)";echo "-harm   : Highest order of periodic signal in matching";echo " ";echo "#  FOR EXAMPLE :";echo "$ . Matching_PSRCAT_auto.bash -radecd 3 -p0d 0.5 -dmd 100 -harm 16";echo " ";echo "(or using simple form at of default parameters:  -radecd 2 -p0d 0.5 -dmd 80 -harm 16)";echo "$ . Matching_PSRCAT_auto.bash -def";echo " ";;
      -def) DEF=1;;
      -*) echo "*  Warning : the '$1' may not an option ";;
      esac
      shift
done

if [[ "${HELP}" = "0" ]]; then    # HELP
if [[ "${DEF}" = "1" ]]; then
   ERRORdeg=2
   ERRORp0=0.5
   ERRORdm=80
   HARMmax=16
fi

echo " "
echo "# Matching region :"
echo " "
echo "RA and DEC deviation (degree)  = ${ERRORdeg}"
echo "Rotation Period deviation (ms) = ${ERRORp0}"
echo "DM deviation (pc * cm^-3)      = ${ERRORdm}"
echo "Highest order in matching      = ${HARMmax}"
echo "PSR-num.in'PSR_17.08.27.list'   = ${NUMPSR}"

ROW=`awk '{print NR}' DataList | tail -n1`
echo "Cands number in DataList  = ${ROW}"
echo " "

for((ii=1 ; ii<=${ROW} ; ii++)) ; do        # Loop for DataList

   RAIN=0
   DECIN=0
   P0IN=0
   DMIN=0
   BREAK=0
   PRECENT=0

   FNAME=`cat DataList | sed -n "${ii}p" | awk '{print $1}'`
   RAIN=`cat DataList | sed -n "${ii}p" | awk '{print $2}'`
   DECIN=`cat DataList | sed -n "${ii}p" | awk '{print $3}'`
   P0IN=`cat DataList | sed -n "${ii}p" | awk '{print $4}'`
   DMIN=`cat DataList | sed -n "${ii}p" | awk '{print $5}'`

#   echo "FNAME  = ${FNAME}"
#   echo "RAIN   = ${RAIN}"
#   echo "DECIN  = ${DECIN}"
#   echo "P0IN   = ${P0IN}"
#   echo "DMIN   = ${DMIN}"

   if [[ "${P0IN}" = "0" ]]||[[ "${DMIN}" = "0" ]]||[[ "${RAIN}" = "0" ]]||[[ "${DECIN}" = "0" ]]||[[ "${ERRORdeg}" = "0" ]]||[[ "${ERRORp0}" = "0" ]]||[[ "${ERRORdm}" = "0" ]]||[[ "${HARMmax}" = "0" ]]     ; then
      BREAK=1
      if [[ "${HELP}" = "0" ]]; then
         echo " "
         echo "*  Input options are not enough, please include all items as follows:"
         echo "   ————————————————————————————————————————————————————————————————— "
         echo "-radecd : Position deviation in RA and DEC (degree)"
         echo "-p0d    : Period deviation in p0 (ms)"
         echo "-dmd    : Dispertion measure deviation in (pc * cm^-3)"
         echo "-harm   : Highest order of periodic signal in matching"
         echo "-ra     : RA(degree) of PSR candidate"
         echo "-dec    : DEC(degree) of PSR candidate"
         echo "-p0     : Period(ms) of PSR candidate"
         echo "-dm     : DM of PSR candidate"
         echo " "
      fi
   fi
  
  
   if [[ "${BREAK}" = "0" ]]; then
      echo " "
      echo "Run ${FNAME} ... ...   ${ii} / ${ROW}"
      echo "RA  = ${RAIN}"
      echo "DEC = ${DECIN}"
      echo "P0  = ${P0IN}"
      echo "DM  = ${DMIN}"  
      echo " "

 # Matching region of RA & DEC
 # (RA)
   END=0
   RALO=`echo "${RAIN}-${ERRORdeg}" | bc`
   RAHI=`echo "${RAIN}+${ERRORdeg}" | bc`
  
   RALOR=`cat PSR_17.08.27.list | sed "${1}q;d" | awk '{print $3}'`
   RAHIR=`cat PSR_17.08.27.list | sed "${NUMPSR}q;d" | awk '{print $3}'`
   if [[ `echo "${RALO}<${RALOR}" | bc` -eq 1 ]]; then
      RALO=${RALOR}
   fi
   if [[ `echo "${RAHI}>${RAHIR}" | bc` -eq 1 ]]; then
      END=1
   fi
   RALO=`echo "scale=0; ${RALO} /1"| bc`
  
  
   RAMASK1="2 4 9 20 35 36 38 39 44 45 48 49 56 58 67 70 71 76 87 94 100 102 106 108 120 144 314 323 357"
   MASK1=(${RAMASK1})
   for ((m=0 ; m<=28 ; m++)) ; do
       if [[ "${RALO}" = "${MASK1[m]}" ]]; then
          RALO=`echo "${RALO}-1" | bc`
       fi
       if [[ "${RAHI}" = "${MASK1[m]}" ]]; then
          RAHI=`echo "${RAHI}+1" | bc`
       fi
   done

   if [[ `echo "${RALO}<${RALOR}" | bc` -eq 1 ]]; then
      RALO=${RALOR}
   fi
   if [[ `echo "${RAHI}>${RAHIR}" | bc` -eq 1 ]]; then
      END=1
   fi
   RALO=`echo "scale=0; ${RALO} /1"| bc`
   RAHI=`echo "scale=0; ${RAHI} /1"| bc`
#echo "RALO = ${RALO}  RAHI = ${RAHI}"
 
   if [[ `echo "${RALO}>=${RAHI}" | bc` -eq 1 ]]; then
      echo "*  No known pulsars RA in region of ${RAIN}+-${ERRORdeg}"
      echo " "
   else
      if [[ "${END}" = "0" ]]; then
         NUMRALO=`cat PSR_17.08.27.list | awk '{print $3}' | cat -n | grep "${RALO}\." | sed "${1}q;d" | awk '{print $1}'`
         NUMRAHI=`cat PSR_17.08.27.list | awk '{print $3}' | cat -n | grep "${RAHI}\." | sed "${1}q;d" | awk '{print $1}'`
      elif [[ "${END}" = "1" ]]; then
         NUMRALO=`cat PSR_15.11.2.list | awk '{print $3}' | cat -n | grep "${RALO}\." | sed "${1}q;d" | awk '{print $1}'`
         NUMRAHI=`echo "${NUMPSR}"`
      fi
#echo "NUMRALO = ${NUMRALO}   NUMRAHI = ${NUMRAHI}"
      LINE=0
      for ((i=${NUMRALO} ; i<=${NUMRAHI} ; i++)) ; do
          if [[ "${i}" = "${NUMRALO}" ]]; then
             cat PSR_17.08.27.list | sed "${i}q;d" | cat > temp1
          else
             cat PSR_17.08.27.list | sed "${i}q;d" | cat >> temp1
          fi
          LINE=`echo "${LINE}+1" | bc`
      done
 
 
#(DEC)
      LINEDEC=0
      DECGOOD=0
      for (( j=1 ; j<=${LINE} ; j++ )) ; do
	  RAR=`cat temp1 | sed "${j}q;d" | awk '{print $3}'`
          DECR=`cat temp1 | sed "${j}q;d" | awk '{print $4}'`
#         echo "j = ${j}  DECR = ${DECR}"
          if [[ `echo "${DECR}-(${DECIN})<=${ERRORdeg}" | bc` -eq 1 ]] && [[ `echo "${DECIN}-(${DECR})<=${ERRORdeg}" | bc` -eq 1 ]]; then
             if [[ "${j}" = "1" ]]; then
                cat temp1 | sed "${j}q;d" | cat > temp2
             else
                cat temp1 | sed "${j}q;d" | cat >> temp2
             fi
             DECGOOD=1
             LINEDEC=`echo "${LINEDEC}+1" | bc`
          fi
      done
      if [[ "${DECGOOD}" = "1" ]]; then
         echo "*  ${LINEDEC} known PSRs located in (RA = ${RAIN}, DEC = ${DECIN}) +- ${ERRORdeg} degree"
         echo " "
      else
         echo "*  No known pulsars of RA & DEC in region of (RA = ${RAIN}, DEC = ${DECIN}) +- ${ERRORdeg} degree"
         echo " "
      fi


      if [[ "${DECGOOD}" = "1" ]]; then   # DECGOOD
	 ERRDIS2=0
	 ERRDIS=0
 

# Matching P0 & DM
#(DM)
         LINEDM=0
         for (( k=1 ; k<=${LINEDEC} ; k++ )) ; do
             DMR=`cat temp2 | sed "${k}q;d" | awk '{print $6}'`
 
             if [[ "${DMR}" = "*" ]]; then
                DMR=0
             fi
#            echo "DMR = ${DMR}"
             if [[ `echo "${DMR}-(${DMIN})<=${ERRORdm}" | bc` -eq 1 ]] && [[ `echo "${DMIN}-(${DMR})<=${ERRORdm}" | bc` -eq 1 ]]; then
                if [[ "${k}" = "1" ]]; then
                   cat temp2 | sed "${k}q;d" | cat > temp3
                else
                   cat temp2 | sed "${k}q;d" | cat >> temp3
                fi
                DMGOOD=1
                LINEDM=`echo "${LINEDM}+1" | bc`
             fi
         done
  
         if [[ "${DMGOOD}" = "1" ]]; then   # DMGOOD
 
#(P0)
            if [[ "${ii}" = "1" ]]; then
               echo "                             file                          Jname       DELTA_(deg)   DELTA_P0(ms)    DELTA_DM      Num of Harm." > matching.list
            fi

            OUTPUT=0
  
            for ((l=1 ; l<=${LINEDM} ; l++)) ; do                                    # comp.1
                echo "Matching PSR harmonic wave, in Loop ${l} / ${LINEDM}"
                DMRR=`cat temp3 | sed "${l}q;d" | awk '{print $6}'`
                P0R=`cat temp3 | awk '{print $5*1000}' | sed "${l}q;d"`
                if [[ "${DMRR}" = "*" ]]; then
		   DMRR=0
	        fi

                if [[ `echo "${P0R}-${P0IN}<=${ERRORp0}" | bc` -eq 1 ]] && [[ `echo "${P0IN}-${P0R}<=${ERRORp0}" | bc` -eq 1 ]] ; then
                                                                                     # comp.2
                   DELTADM=`echo "${DMRR}-(${DMIN})" | bc`
                   DELTAP0=`echo "scale=3 ; ${P0R}-${P0IN}" | bc`
                   PRECENT=`echo "scale=1 ; 100 * ${DELTAP0} / ${P0R}" | bc`
		   PRECENT=`echo ${PRECENT#-}`
                   HARM1=1
                   HARM2=1
                   OUTPUT=1
                   PSR=`cat temp3 | sed "${l}q;d" | awk '{print $2}'`

                   RAR=`cat temp3 | sed "${l}q;d" | awk '{print $3}'`
	           DECR=`cat temp3 | sed "${l}q;d" | awk '{print $4}'`
                   ERRRA=`echo "${RAR}-(${RAIN})" | bc`
	           ERRDEC=`echo "${DECR}-(${DECIN})" | bc`
	           ERRDIS2=`echo "${ERRRA}*(${ERRRA}) + (${ERRDEC})*(${ERRDEC})" | bc`
	           ERRDIS=`echo "scale=2 ; sqrt(${ERRDIS2}) /1" | bc`
#	 echo "$RAR  $RAIN  $DECR  $DECIN  ...  $ERRRA   $ERRDEC   $ERRDIS2   $ERRDIS"


                   HARM=`echo "1st. of PSR ${PSR}"`
                   STATE="${ERRDIS}     ${DELTAP0} (${PRECENT}%)      ${DELTADM}        ${HARM}"
                   echo "${FNAME}   ${PSR}         ${STATE}" | cat >> matching.list
 
                else
                   for (( HARM1=1 ; HARM1<=${HARMmax} ; HARM1++ )) ; do              # comp.3
                   for (( HARM2=1 ; HARM2<=${HARMmax} ; HARM2++ )) ; do              # comp.4 
                   if [[ "${HARM1}" = "1" ]] || [[ "${HARM2}" = "1" ]]; then         # comp.5
                      P0harmR=`echo "scale=3 ; ${P0R} / ${HARM1}" | bc`
                      P0harmI=`echo "scale=3 ; ${P0IN} / ${HARM2}" | bc`
                      DELTADM=`echo "${DMRR}-(${DMIN})" | bc`
                      DELTAP0=`echo "scale=3 ; ${P0harmR}-${P0harmI}" | bc`
		      PRECENT=`echo "scale=1 ; 100 * ${DELTAP0} / ${P0R}" | bc`
		      PRECENT=`echo ${PRECENT#-}`
#                     echo "${P0harmR}   ${P0harmI}"
                      if [[ `echo "${P0harmR}-${P0harmI}<=${ERRORp0}" | bc` -eq 1 ]] && [[ `echo "${P0harmI}-${P0harmR}<=${ERRORp0}" | bc` -eq 1 ]] ; then
                         OUTPUT=1
                         PSR=`cat temp3 | sed "${l}q;d" | awk '{print $2}'`

                         RAR=`cat temp3 | sed "${l}q;d" | awk '{print $3}'`
                   	 DECR=`cat temp3 | sed "${l}q;d" | awk '{print $4}'`
                         ERRRA=`echo "${RAR}-(${RAIN})" | bc`
                	 ERRDEC=`echo "${DECR}-(${DECIN})" | bc`
	                 ERRDIS2=`echo "${ERRRA}*(${ERRRA}) + (${ERRDEC})*(${ERRDEC})" | bc`
                 	 ERRDIS=`echo "scale=2 ; sqrt(${ERRDIS2}) /1" | bc`
#	 echo "$RAR  $RAIN  $DECR  $DECIN  ...  $ERRRA   $ERRDEC   $ERRDIS2   $ERRDIS"

                         if [[ `echo "${HARM2}-${HARM1}>0" | bc` -eq 1 ]]; then
                            HARM=`echo "L ${HARM2}"`
                         else
                            HARM=`echo "H ${HARM1}"`
                         fi
 
                         STATE="${ERRDIS}     ${DELTAP0} (${PRECENT}%)      ${DELTADM}        ${HARM}"
                         echo "${FNAME}    ${PSR}         ${STATE}" | cat >> matching.list
                      fi
                   fi         # end comp.5
 
                   done       # end comp.4
                   done       # end comp.3
                fi            # end comp.2
            done              # end comp.1
         fi                   # DMGOOD
 
         if [[ "${OUTPUT}" = "1" ]]; then
            echo "————————————————————————————————————————————————————————————————"
            echo " " 
            echo "                             file                          Jname       DELTA_(deg)   DELTA_P0(ms)    DELTA_DM      Num of Harm."
            cat matching.list | grep -v "Jname" | cat -n
            echo " "
            echo "————————————————————————————————————————————————————————————————"
#           psrcat -e ${PSR}
         else
            echo "————————————————————————————————————————————————————————————————"
            echo " "
            echo "No known pulsars of P0 & DM in region of ${P0IN}+-${ERRORp0} & ${DMIN}+-${ERRORdm}"
            echo " "
            echo "————————————————————————————————————————————————————————————————"
         fi
 
         rm temp*
 
      fi   # DECGOOD
   fi
   fi   # break
done   # Loop for DataList
fi   # HELP
