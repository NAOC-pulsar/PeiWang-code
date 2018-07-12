import numexpr as ne

import numpy as np


class FitsWeighting:
    def Gvalue(self,dec, tau, totalTime, nsblk, nsubint, float_freq):
        c = 299794580.0
        pi = np.pi
        d = 300
        F=1
        omega = 2*pi / 3600.000 / 24.000

        float_freq1 = float_freq[0]

        float_time = np.float32(np.linspace(0, totalTime, nsblk * nsubint))

        float_time = float_time - tau

        float_time = float_time.reshape(float_time.size, 1)

        float_freq1 = float_freq1.reshape(1, float_freq1.size)

        eta = np.dot(float_time, float_freq1)  # matrix element
        print '1'
        pi=np.pi

        eta = ne.evaluate("((-2 * pi * omega * d * 1000000) / (1.22 * c)) * (eta)")

        tem = np.cos(dec * 2 * np.pi / 360)
        #for i in range(0,self.numSubint, self.numSubint):  # split freq.range into segments
        etatmp = eta[:,:]
        etatmp = ne.evaluate("(sin(etatmp)/etatmp)**2")
        eta[:, :] = ne.evaluate("(F*tem*etatmp)")

        return eta


    def weighting(self, dec, tau, totalTime,float_data,nsblk, numSubint, float_dat_freq,):
        etas = self.Gvalue(dec, tau, totalTime, nsblk, numSubint, float_dat_freq,float_data)

        etas = etas.reshape(self.numSubint, self.nsblk, 1, self.chnum, 1)
        # for k in range(0, self.numSubint, self.numSubint):
        temdata = self.float_data2
        temg = etas
        self.float_data2 = ne.evaluate("temg*temdata")
        self.float_data2 = np.uint8(self.float_data2)
        self.float_data2 = temg
