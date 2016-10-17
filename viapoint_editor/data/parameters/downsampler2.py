# -*- coding: utf-8 -*-

from parameters import *

import numpy as np
import scipy.signal as signal

DOWNSAMPLER_TYPE = 1001

class DownsamplerParameter(IParameter):

    def __init__(self):

        IParameter.__init__(self, "60 Hz Down-Sampler 2", DOWNSAMPLER_TYPE)        
	
    def applyParameter(self, data):

        frame_size = self.getHiddenVariable('SIGNAL_RATE');
        factor = frame_size / 60.0
        
        new_data = signal.decimate(data, int(np.floor(factor)))

        self.setHiddenVariable('SIGNAL_SIZE', new_data.size)
        self.setHiddenVariable('SIGNAL_RATE', 60.0)
        
        return new_data


def loadParameter():

    downsampler = DownsamplerParameter()
    return downsampler
