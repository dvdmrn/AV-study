# -*- coding: utf-8 -*-

from parameters import *

import numpy as np

NORMALIZER_TYPE = 1006
DEFAULT_FACTOR = 1.0

class Normalizer(IParameter):

    def __init__(self):

        IParameter.__init__(self, "Normalizer", NORMALIZER_TYPE)
        self.setVariable("SCALE", DEFAULT_FACTOR)
	
    def applyParameter(self, data):

        val = max(abs(data.max()), abs(data.min()))

        normalized = data * (self.getVariable("SCALE") / val)
        return normalized
    

def loadParameter():

    return Normalizer()
