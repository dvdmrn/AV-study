# -*- coding: utf-8 -*-

from parameters import *

from scipy.fftpack import rfft, irfft, rfftfreq

import numpy as np

import matplotlib.pylab as plt

DOWNSAMPLER_TYPE = 1001

class DownsamplerParameter(IParameter):

    def __init__(self):

        IParameter.__init__(self, "60 Hz Down-Sampler", DOWNSAMPLER_TYPE)        
	
    def applyParameter(self, data):

        frame_size = self.getHiddenVariable('AUDIO_FRAME_SIZE');
        window = np.ones(frame_size)/float(frame_size)
        indexes = np.s_[::frame_size]

        downsampled_data = data[indexes]

        self.setHiddenVariable('SIGNAL_SIZE', data.size)
        self.setHiddenVariable('SIGNAL_RATE', 60.0)
        
        return downsampled_data


def loadParameter():

    downsampler = DownsamplerParameter()
    return downsampler
