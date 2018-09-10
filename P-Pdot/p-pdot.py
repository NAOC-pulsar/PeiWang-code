# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import xlrd

xdins=[l.replace('E','e').replace('?','-') for l in open('XDINS.txt')]
#fast=[l.replace('E','e').replace('?','-') for l in open('fast.txt')]
magnetar=[l.replace('E','e').replace('?','-') for l in open('MAGNETAR.txt')]
normal=[l.replace('E','e').replace('?','-') for l in open('NORMAL.txt')]
rrat=[l.replace('E','e').replace('?','-') for l in open('RRAT.txt')]
binary=[l.replace('E','e').replace('?','-') for l in open('BINARY.txt')]
msp=[l.replace('E','e').replace('?','-') for l in open('MSP.txt')]
fast=xlrd.open_workbook('fast.xlsx')
xls_sheet0 = fast.sheets()[0]
xls_sheet1 = fast.sheets()[1]

p1=[float(l.split()[0])for l in binary]
pdot1=[float(l.split()[1])for l in binary]
p2=[float(l.split()[0])for l in magnetar]
pdot2=[float(l.split()[1])for l in magnetar]
p3=[float(l.split()[0])for l in normal]
pdot3=[float(l.split()[1])for l in normal]
p4=[float(l.split()[0])for l in rrat]
pdot4=[float(l.split()[1])for l in rrat]
p5=[float(l.split()[0])for l in xdins]
pdot5=[float(l.split()[1])for l in xdins]
p6=[float(l.split()[1])for l in msp]
pdot6=[float(l.split()[2])for l in msp]
p7=np.array(xls_sheet0.col_values(1))/1000
pdot7=xls_sheet0.col_values(2)
p8=np.array(xls_sheet1.col_values(1))/1000
pdot8=xls_sheet1.col_values(2)

p=np.arange(0.001,20,0.1)
B1=3.2**-2*1e-10/p
B2=3.2**-2*1e-14/p
B3=3.2**-2*1e-18/p
B4=3.2**-2*1e-22/p
N1=1.585*1e-12*p
N2=1.585*1e-14*p
N3=1.585*1e-16*p
N4=1.585*1e-18*p
E1=1e8*(p**3*1e15)/(3.95*1e31)
E2=1e7*(p**3*1e15)/(3.95*1e31)
E3=1e6*(p**3*1e15)/(3.95*1e31)
E4=1e5*(p**3*1e15)/(3.95*1e31)
E5=1e4*(p**3*1e15)/(3.95*1e31)
E6=1e3*(p**3*1e15)/(3.95*1e31)
E7=1e2*(p**3*1e15)/(3.95*1e31)
E8=1e1*(p**3*1e15)/(3.95*1e31)
E9=1e0*(p**3*1e15)/(3.95*1e31)

fig=plt.figure()
ax=fig.add_subplot(111)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(5e-22,1e-3)
ax.set_xlim(1e-3,20)

l1=ax.scatter(p1,pdot1,c='r',marker='o',alpha=0.5,cmap=plt.cm.Blues,edgecolor='none',label='BINARY',s=40)
l2=ax.scatter(p2,pdot2,c='b',marker='^',alpha=0.5,cmap=plt.cm.Blues,edgecolor='none',label='MAGNETAR',s=50)
l3=ax.scatter(p3,pdot3,c='k',marker='.',alpha=0.7,cmap=plt.cm.Blues,edgecolor='none',label='NORMAL',s=20)
l4=ax.scatter(p4,pdot4,c='g',marker='s',alpha=0.6,cmap=plt.cm.Blues,edgecolor='none',label='RRAT',s=50)
l5=ax.scatter(p5,pdot5,c='c',marker='*',alpha=0.5,cmap=plt.cm.Blues,edgecolor='none',label='XDINS',s=60)
l6=ax.scatter(p6,pdot6,c='',marker='o',alpha=0.5,cmap=plt.cm.Blues,label='MSP',s=20)
l6dot=ax.scatter(p6,pdot6,c='k',marker='.',alpha=0.5,cmap=plt.cm.Blues,edgecolor='none',s=20)
l7=ax.scatter(p7,pdot7,c='m',marker='_',alpha=0.6,cmap=plt.cm.Blues,edgecolor='m',linewidths=1,label='FAST(upper_limit)',s=150)
l8=ax.scatter(p8,pdot8,c='w',marker='*',alpha=1,cmap=plt.cm.Blues,edgecolor='m',linewidths=2.5,label='FAST(timing)',s=150)

ax.plot(p,B1,'--k',alpha=0.5) #B=10^14Gauss
ax.plot(p,B2,'--k',alpha=0.5) #B=10^12Gauss
ax.plot(p,B3,'--k',alpha=0.5) #B=10^10Gauss
ax.plot(p,B4,'--k',alpha=0.5) #B=10^8Gauss
ax.plot(p,N1,':k',alpha=0.5)  #T=10^4yr
ax.plot(p,N2,':k',alpha=0.5)  #T=10^6yr
ax.plot(p,N3,':k',alpha=0.5)  #T=10^8yr
ax.plot(p,N4,':k',alpha=0.5)  #T=10^10yr
ax.plot(p,E1,'-.r',alpha=0.9)  #Edot=10^38erg/s
ax.plot(p,E2,'-.r',alpha=0.9)  #Edot=10^37erg/s
ax.plot(p,E3,'-.r',alpha=0.9)  #Edot=10^36erg/s
ax.plot(p,E4,'-.r',alpha=0.9)  #Edot=10^35erg/s
ax.plot(p,E5,'-.r',alpha=0.9)  #Edot=10^34erg/s
ax.plot(p,E6,'-.r',alpha=0.9)  #Edot=10^33erg/s
ax.plot(p,E7,'-.r',alpha=0.9)  #Edot=10^32erg/s
ax.plot(p,E8,'-.r',alpha=0.9)  #Edot=10^31erg/s
ax.plot(p,E9,'-.r',alpha=0.9)  #Edot=10^30erg/s

ax.text(0.0012,1e-8, r'$B_s = 10^{14} G$',alpha=0.8, rotation=-8)
ax.text(0.0011,1e-12, r'$10^{12} G$',alpha=0.8, rotation=-8)
ax.text(0.0011,1e-16, r'$10^{10} G$',alpha=0.8, rotation=-8)
ax.text(0.0011,1e-20, r'$10^{8} G$',alpha=0.8, rotation=-8)
ax.text(0.007,3e-14, r'$\tau$ = $10000 yr$',alpha=0.9, rotation=9)
ax.text(0.01,3e-16, r'$10^6 yr$',alpha=0.9, rotation=9)
ax.text(0.01,3e-18, r'$10^8 yr$',alpha=0.9, rotation=9)
ax.text(0.01,0.9e-20, r'$10^{10} yr$',alpha=0.9, rotation=9)
ax.text(6,6e-6, r'$\dot{E}$ = $10^{38} erg/s$',color='r',alpha=0.9, rotation=30)
ax.text(10,7e-8, r'$10^{36}$',color='r',alpha=0.9, rotation=30)
ax.text(10,7e-10, r'$10^{34}$',color='r',alpha=0.9, rotation=30)
ax.text(10,7e-12, r'$10^{32}$',color='r',alpha=0.9, rotation=30)
ax.text(10,7e-14, r'$10^{30}$',color='r',alpha=0.9, rotation=30)
ax.legend(handles = [l1,l2,l3,l4,l5,l6,l7,l8], labels = [], loc = 'upper left')
plt.annotate('Upper limit', xy=(0.2, 1e-9), xytext=(0.2, 1e-7), alpha=0.2, color='m', arrowprops=dict(facecolor='m', alpha=0.2, edgecolor='none', shrink=50))
plt.xlabel('Rotation Period  (s)')
plt.ylabel('dP/dt  (s/s)')
plt.show()
