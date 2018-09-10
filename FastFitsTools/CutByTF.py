
from FastFitsTools.FitsTools import Fitscut, Fits
from FastFitsTools.FitsTools.FitsOutput import wirtreToFileForFast


def usage():
    print """

"-f", "file:      [ please give ***path/filename*** ]"
"-b", "beginfreq: [ start freq ]"
"-e", "endfreq:   [ end freq ]"
"-t", "strattime: [ start time ]"
"-v", "endtime:   [ end time ]"
"-d", "dec(J2000):[ dd:mm:ss ]"
"-o", "output:    [ output path ]"

"""



def exeCutFreq(filename, startfreq, endfreq, initaltime, finaltime, dec, output):
    fits=Fits(filename)
    fits.centerFreq = (startfreq + endfreq) / 2

    fcut=Fitscut( fits,startfreq, endfreq, initaltime, finaltime)
    # self.mergePolae(0)
    fits_cuted=fcut.cut(dec)

    wirtreToFileForFast(fits_cuted,filename,1,outpath)




if __name__ == '__main__':
    import getopt, sys

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:m:f:b:e:o:z:c:t:v:i:s:l:x:y:d:",
                                   ["help", "mode=", "file=", "beginfreq=",
                                    "endfreq=", "output=", "outname", "strattime=", "endtime", "interval=",
                                    "freqspace=","subintoffset=","Fa","Fb","dec="])

    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    if len(sys.argv) == 1:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-m", "--mode"):
            mode = str(a)
        if o in ("-f", "--file"):
            filename = str(a)
        if o in ("-b", "--beginfreq"):
            startfreq = float(a)
        if o in ("-e", "--endfreq"):
            endfreq = float(a)
        if o in ("-o", "--output"):
            outpath = str(a)
        if o in ("-z", "--outname"):
            outname = str(a)
            # print outname
        if o in ("-c", "--cutid"):
            cutid = int(a)
        if o in ("-t", "--strattime"):
            starttime = float(a)
            # print starttime
        if o in ("-v", "--endtime"):
            endtime = float(a)
        if o in ("-i", "--interval"):
            interval = float(a)
        if o in ("-s", "--freqspace"):
            freqSpace = int(a)

        if o in ("-l", "--subintoffset"):
            subintoffset = int(a)
        if o in ("-d", "--dec"):
            dec = str(a)
        if o in ("-x", "--Fa"):
                aa = float(a)
        if o in ("-y", "--Fb"):
                bb = float(a)

    exeCutFreq(filename, startfreq, endfreq, starttime, endtime, dec, output)



