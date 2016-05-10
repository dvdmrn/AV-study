# -*- coding: utf-8 -*-

from parameters import *

import numpy as np

OFFSET_TYPE = 1007
DEFAULT_OFFSET = -1.0

class Offset(IParameter):

    def __init__(self):

        IParameter.__init__(self, "Offset", OFFSET_TYPE)
        self.setVariable("OFFSET", DEFAULT_OFFSET)
	
    def applyParameter(self, data):

        offset = data + self.getVariable("OFFSET")
        return offset


def loadParameter():

    return Offset()
