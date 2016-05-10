# -*- coding: utf-8 -*-

from parameters import *

from scipy.fftpack import rfft, irfft, rfftfreq

import numpy as np

import matplotlib.pylab as plt

LPF_TYPE = 1001
DEFAULT_LPF_FILTER_FREQUENCY_HZ = 20


class AccurateLPF(IParameter):

    def __init__(self):

        #Initializes class as a parameter
        IParameter.__init__(self, "Ideal LPF", LPF_TYPE)

        self.setVariable("FREQUENCY", DEFAULT_LPF_FILTER_FREQUENCY_HZ)

    def applyParameter(self, data):

        rate = self.getHiddenVariable('AUDIO_FRAME_RATE')

        print rate, self.getVariable("FREQUENCY")
        
        #low pass filter
        fftdata = rfft(data.clip(0))

        frequencies = rfftfreq(fftdata.size, (1.0/rate))
        index = np.where(frequencies >= self.getVariable("FREQUENCY"))[0][0]
        
        fftdata[index+1:] = 0

        ##removes negative values
        filtered_data = irfft(fftdata)

        
        return filtered_data


def loadParameter():

    lpf = AccurateLPF()
    return lpf
