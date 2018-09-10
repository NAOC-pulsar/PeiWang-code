import fitsio
import os, sys

filename = sys.argv[1]

hdulist = fitsio.FITS(filename, 'rw')
hdulist[0].write_key('RA', '17:17:07.39')
hdulist[0].write_key('DEC', '43:08:09.4')

hdulist.close()
