import numpy as np
def mergePolae(fits):
    # self.Npolae = 1
    # if self.flag == 0:
    if fits.Npolae > 1:
        fits.float_data = np.array(fits.float_data[:, :, 0, :, :])
        fits.Npolae = 1
    # if self.flag == 1:
    #     float_data_1 = np.array(self.float_data_1[:, :, 0, :, :])
    #     float_data_2 = np.array(self.float_data_2[:, :, 0, :, :])
    #     self.float_data = np.concatenate((float_data_1, float_data_2))
    #     self.Npolae = 1
        # self.float_data=self.float_data3[:,:,0,:,:]+self.float_data3[:,:,1,:,:]