#!/usr/bin/env python
import numpy as np
import fitsio
import sys
import math
import commands
#from astropy.io import fits
#from astropy.table import Table



#---------------
#beam weight
def beamWeight(filename, scale, percent, flag, plotset):
    #settings
    C = 299794580.0
    D = 300.0
    #Pi = 3.141592654
    Pi = math.pi
    Omega = 2.*Pi/3600./24.
    Filename = filename
    Scale = scale
    Percent = percent
    Flag = flag

    #read file 
    hdulist = fitsio.FITS(Filename, 'rw')
    hdu1 = hdulist[1]
    hdu0 = hdulist[0]
    header1 = hdu1.read_header()
    header0 = hdu0.read_header()
    data1=hdulist[1][:]
    Time_subint = header1['TBIN']*header1['NSBLK']
    Freq_start = header0['OBSFREQ']-header0['OBSBW']/2.
    Freq_chann = header0['OBSBW']/header0['OBSNCHAN']
    
    Nsub = np.array(data1['DAT_WTS']).shape[0]
    Nchan = np.array(data1['DAT_WTS']).shape[1]
    Tau = round(Time_subint * Nsub * Percent)	
    Weight = np.zeros((Nsub,Nchan))
    
    for isub in range(0,Nsub):
        Time = Time_subint * isub
        for ichan in range(0,Nchan):
            Freq = Freq_start + ichan*Freq_chann
            if (Flag == 1):
                Weight[isub,ichan] = 1
            else :
                Eta = -2.*Pi*Omega*(Time-Tau)/(1.22*(C/Freq/1000000.)/D)
                Weight[isub,ichan] = Scale*(math.sin(Eta)/Eta)**2.
#                    Weight[isub,ichan] = Scale*math.cos(Dec*2.*Pi/360.)*(math.sin(Eta)/Eta)**2.
    print Weight.shape
    if (Flag == 1):
        Dat_wts = Weight
    else :
        Dat_wts = data1['DAT_WTS']*Weight
    hdu1.write_column('DAT_WTS', Dat_wts)
    hdulist.close()
    print 'DAT_WTS[',int(Nsub*Percent),',',Nchan,']=', data1['DAT_WTS'][int(Nsub*Percent),Nchan-1], '->', Dat_wts[int(Nsub*Percent),Nchan-1]
    print 'DAT_WTS[',Nsub,',',Nchan,']=', data1['DAT_WTS'][Nsub-1,Nchan-1], '->', Dat_wts[Nsub-1,Nchan-1]
    if (plotset == 1):
        plotWeight(Nsub, Nchan, Dat_wts)



#-------------------------------
#plot the weight
def plotWeight(Nsub, Nchan, Weight):
    from matplotlib import pyplot as plt 
    from mpl_toolkits.mplot3d import Axes3D 
    fig = plt.figure() 
    ax = Axes3D(fig) 
    X = range(0, Nsub) 
    Y = range(0, Nchan) 
    X, Y = np.meshgrid(X, Y) 
    Z = Weight
    ax.plot_surface(X, Y, Z.T, rstride=1, cstride=1, cmap='rainbow') 
    plt.show()


if __name__ == "__main__":
    
    #check input
    Flag = 0
    if (len(sys.argv)==2):
        #Fitslist = sys.argv[1]
        #Flag = 1 mean reset the weight
        Flag = 1
        plotset = 0
        Scale = 0
        Percent = 0
        Filename = sys.argv[1]
        print 'Reset for the "DAT_WTS"'
        beamWeight(Filename, Scale, Percent, Flag, plotset) 

    elif (len(sys.argv) == 4):
        #elif (len(sys.argv) == 5):
        Flag = 0
        plotset = 0
        Scale = float(sys.argv[1])     # Between 0 and 1
        Percent = float(sys.argv[2])   # Between 0 and 1
        Filename = sys.argv[3]
        beamWeight(Filename, Scale, Percent, Flag, plotset) 

    elif (len(sys.argv) == 5):
        Flag = 0
        plotset = 0
        Scale = float(sys.argv[1])     # Between 0 and 1
        Percent = float(sys.argv[2])   # Between 0 and 1
        Filename = sys.argv[3]
        plotset = int(sys.argv[4])
        beamWeight(Filename, Scale, Percent, Flag, plotset) 

    else :
        print 'Wrong inputs!'
        print 'Weight Usage: python *.py Scale(0-1) Time_percent(0-1) filename plotset(1)'
        print 'Weight Usage: python *.py Scale(0-1) Time_percent(0-1) filename'
        print 'Reset  Usage: python *.py filename'
        sys.exit()
    
#-----------------------------------------------------------------------------------------------

