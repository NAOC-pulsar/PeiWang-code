def Gvalue(self, dec, tau, totalTime, nsblk, nsubint, float_freq, a, b):
    c = 299794580.0
    pi = np.pi
    d = 300
    F = b

    tau -= 5
    omega = 2 * pi / 3600.000 / 24.000

    float_freq1 = float_freq[0]

    float_time = np.linspace(0, totalTime, nsblk * nsubint)

    float_time = float_time - tau

    float_time = float_time.reshape(float_time.size, 1)

    float_freq1 = float_freq1.reshape(1, float_freq1.size)

    eta = np.dot(float_time, float_freq1)  # matrix element
    print '1'
    pi = np.pi

    eta = ne.evaluate("((-2 * pi * omega * d * 1000000) / (1.22 * c)) * (eta)")

    tem = np.cos(dec * 2 * np.pi / 360)
    # for i in range(0,self.numSubint, self.numSubint):  # split freq.range into segments
    etatmp = eta[:, :]
    etatmp = ne.evaluate("(sin(etatmp)/etatmp)**2")
    eta[:, :] = ne.evaluate("(F*tem*etatmp)")

    return eta

def weighting(self,etas ,a,b):

    #for k in range(0, self.numSubint, self.numSubint):
    temdata = self.float_data2
    ran=temdata.max()/128
    temdata=temdata/ran
    avg=np.mean(temdata)
    temdata=temdata-(avg*0.5)
    temdata[temdata<0]=0
    temg = etas +a
    self.float_data2 = ne.evaluate("temg*temdata")
    #self.float_data2 = np.uint8(self.float_data2)
    self.float_data2[self.float_data2>255]=255
    self.float_data2=self.float_data2.astype(np.uint8)
