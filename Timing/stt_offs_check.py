# -*- coding: utf-8 -*
#!/usr/bin/env python
import numpy as np 
import pyfits
import sys
#新建filelist.txt文件列表和输出文本output1.txt, output2.txt

output1 = []
output2 = []
filename = np.genfromtxt('filelist.txt',dtype='|S50')
print(filename)
lines = np.shape(filename)[0]-1
print(lines-1)

hdulist = pyfits.open(filename[0])
hdu0 = hdulist[0]
header0 = hdu0.header
hdu1 = hdulist[1]
header1 = hdu1.header
imjd0 = header0['STT_IMJD']
smjd0 = header0['STT_SMJD']
offt0 = header0['STT_OFFS']
Offset0 = header1['NSUBOFFS']

for line in np.linspace(0,lines,lines):
        num = np.int(line)
	hdulist = pyfits.open(filename[num])
	hdu0 = hdulist[0]
	header0 = hdu0.header
	hdu1 = hdulist[1]
	header1 = hdu1.header
	imjd = header0['STT_IMJD']
	smjd = header0['STT_SMJD']
	offt = header0['STT_OFFS']
	Offset = header1['NSUBOFFS']
	#Sample = header1['NSBLK']
	#Tbins = header1['TBIN']
        Offset1 = Offset - 64*num
        if imjd == imjd0 and  smjd == smjd0 and offt == offt0 and Offset1 == Offset0 :
              datwritf=file('output1.txt','a')
              datwritf.write(str(filename[num])+' '+str(imjd)+' '+str(smjd)+' '+str(offt)+' '+str(Offset)+'\n')
        else:
              datwritf1=file('output2.txt','a')
              datwritf1.write(str(filename[num])+' '+str(imjd)+' '+str(smjd)+' '+str(offt)+' '+str(Offset)+'\n')
