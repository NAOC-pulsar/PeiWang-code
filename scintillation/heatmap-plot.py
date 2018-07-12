# -- coding: utf-8 --
#!/usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import axes


filename = np.genfromtxt('filelist.txt',dtype='|S50') #输入列表
print(filename)
lines = np.shape(filename)[0] #列表行数
print(lines)

name = str(filename[0])
a0 = np.loadtxt(name)
h = 2048
w0 = int(a0[a0.shape[0]-1,0])+1
data = np.zeros((w0,h))
for i in range(a0.shape[0]):
    x0 = int(a0[i,0])
    y0 =  int(a0[i,1])
    data[x0,y0]=a0[i,2]

for line in range(lines):
    if line > 0:
        num = np.int(line)
        name = str(filename[num]) #调用文件
        a = np.loadtxt(name)      #将文件转置为数组
        #h = 2048                 #行数为2048
        w = int(a[a.shape[0]-1,0])+1
        w0 = w + w0
        data1 = np.zeros((w,h))
        for i in range(a.shape[0]):
            x1 = int(a[i,0])
            y1 =  int(a[i,1])
            data1[x1,y1]=a[i,2] #给二维数组赋值
#  f = file(filename[num]+'_trans_SNR.txt','a')
# np.savetxt(f,data,fmt='%7.2f')
        data = np.vstack((data,data1))
xlabels = np.zeros(w0)
ylabels = np.zeros(h)
for i in range(w0):
    xlabels[i]=i
for i in range(h):
    ylabels[i] = i
#for i in range(w):
# b[i+1,0]=i
#for i in range(h):
# b[0,i+1]=i

def draw_heatmap(data,xlabels,ylabels):
    #    cmap = cm.Blues
    cmap = cm.get_cmap('RdYlBu_r')
    figure = plt.figure(facecolor='w')
    ax = figure.add_subplot(1,1,1,position=[0.1,0.1,0.1,0.1])
    ax.set_ylabel('sub') #y轴标签
    #ax.set_yticks(range(len(ylabels)))
    #ax.set_yticklabels(ylabels)
    ax.set_xlabel('chan') #x轴标签
    #ax.set_xticks(range(len(xlabels)))
    #ax.set_xticklabels(xlabels)
    ax.set_title(filename[num]) #添加标题
    vmax=data[0][0]
    vmin=data[0][0]
    for i in data:
        for j in i:
            if j>vmax:
                vmax=j
            if j<vmin:
                vmin=j
    map=ax.imshow(data,interpolation='nearest',cmap=cmap,aspect='auto',vmin=vmin,vmax=vmax)
    cb=plt.colorbar(mappable=map,cax=None,ax=None,shrink=0.8)

draw_heatmap(data,xlabels,ylabels)
plt.savefig(filename[0]+'.png')

#plt.show()
print 'finish'


