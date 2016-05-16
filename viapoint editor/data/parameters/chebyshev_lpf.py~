# -*- coding: utf-8 -*-

from parameters import *

from scipy.signal import butter, lfilter

import numpy as np

import matplotlib.pylab as plt

LPF_TYPE = 1003
DEFAULT_LPF_FILTER_FREQUENCY_HZ = 20
DEFAULT_LPF_FILTER_ORDER = 5


class ButterworthLPF(IParameter):

    def __init__(self):

        IParameter.__init__(self, "Butterworth LPF", LPF_TYPE)
        
        self.setVariable("FREQUENCY", DEFAULT_LPF_FILTER_FREQUENCY_HZ)
        self.setVariable("ORDER", DEFAULT_LPF_FILTER_ORDER)

    def butter_lowpass(self, lowcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        b, a = butter(order, low, btype='low')
        return b, a


    def butter_lowpass_filter(self, data, lowcut, fs, order=5):
        b, a = self.butter_lowpass(lowcut, fs, order=order)
        y = lfilter(b, a, data)

        return y

    def applyParameter(self, data):
        
        rate = self.getHiddenVariable('AUDIO_FRAME_RATE')
        print rate, self.getVariable("FREQUENCY")

        filtered_data = self.butter_lowpass_filter(data, self.getVariable("FREQUENCY"), rate, int(self.getVariable("ORDER")))
        
        return filtered_data


def loadParameter():

    lpf = ButterworthLPF()
    return lpf
