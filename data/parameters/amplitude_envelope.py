# -*- coding: utf-8 -*-

from parameters import *

import numpy as np

import matplotlib.pylab as plt

RMS_TYPE = 1004
DEFAULT_AUTO_SIZE = 1
DEFAULT_WINDOW_SIZE = 735

class AmplitudeEnvelope(IParameter):

    def __init__(self):

        IParameter.__init__(self, "Amplitude Envelope Filter", RMS_TYPE)

        self.setVariable("AUTO_SIZE", DEFAULT_AUTO_SIZE)
        self.setVariable("WINDOW_SIZE", DEFAULT_WINDOW_SIZE)

    def windowRMS(self, signal, window_size):
        
        signal_squared = np.power(signal,2)
        window = np.ones(window_size)/float(window_size)
        data = np.sqrt(np.convolve(window, signal_squared, 'valid'))

        return data

    def applyParameter(self, data):

        auto_size = int(self.getVariable("AUTO_SIZE")) == 1

        if (auto_size):
            size = self.getHiddenVariable("AUDIO_FRAME_SIZE")
        else:
            size = self.getVariable("WINDOW_SIZE")
        
        filtered = self.windowRMS(data, size)

        return filtered

def loadParameter():

    envelope = AmplitudeEnvelope()
    return envelope
