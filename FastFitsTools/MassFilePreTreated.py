def exeCutFreqMergeFitsByTime(self, filename, startfreq, endfreq, initaltime, finaltime, i, outpath, dec, fw, a, b):
    self.centerFreq = (startfreq + endfreq - 1) / 2
    # self.checkInputs(startfreq, endfreq, initaltime, finaltime)
    # initaltime = int(round(initaltime / self.timePerSubint)) * self.timePerSubint
    # finaltime = int(round(finaltime / self.timePerSubint)) * self.timePerSubint
    # print self.telecope
    if (self.telecope == 'FAST'):
        startfreqNetNum = int((startfreq - (self.initalFreq - self.chanBW / 2)) * (1. / self.chanBW))

        endfreqNetNum = int((endfreq - (self.initalFreq - self.chanBW / 2)) * (1. / self.chanBW))


        # print '++++++++++++++++',startfreqNetNum,endfreqNetNum
    if (self.Npolae > 1):
        self.mergePolae(0)

    self.cut(startfreqNetNum, endfreqNetNum, initaltime, finaltime)
    self.modifyPHeader(startfreq, endfreq, startfreqNetNum, endfreqNetNum, dec)

    # print startfreqNetNum,endfreqNetNum
    if not fw.any():
        etas = self.Gvalue(self.DecJ_deg, self.totalTime / 4, self.totalTime / 2, self.nsblk, self.numSubint,
                           self.float_dat_freq, a, b)

        etas = etas.reshape(self.numSubint, self.nsblk, 1, self.chnum, 1)
    else:
        etas = fw
    self.weighting(etas, a, b)
    if (self.telecope == 'FAST'):
        if not (os.path.exists(outpath + '/' + filename.split('/')[len(filename.split('/')) - 1][:10])):
            os.mkdir(outpath + '/' + filename.split('/')[len(filename.split('/')) - 1][:10])
        files = filename.split('/')[len(filename.split('/')) - 1]
        #  timelist = {15: 'A', 30: 'B', 60: 'C', 90: 'D', 120: 'E'}
        newpath = outpath + '/' + files[:10] + '/' + \
                  files[:len(files) - 9] + str('%04d' % (int(files[len(files) - 9:len(files) - 5]))) + '_' + str(
            i) + '.fits'
        #                                                           len(files) - 9:len(
        #                                                              files) - 5] + '0' + str(
        #       i) + '.fits'
        # files[:len(files) - 9] + str('%04d' % (int(files[len(files) - 9:len(files) - 5]) + 1))
        self.wirtreToFileForFast(filename, i, newpath)
    return etas
