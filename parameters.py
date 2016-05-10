# -*- coding: utf-8 -*-
import abc

from enum import *

HIDDEN_VARIABLES = ['AUDIO_FRAME_RATE', 'AUDIO_FRAME_COUNT', 'AUDIO_FRAME_SIZE']

class IParameter():

    __metaclass__ = abc.ABCMeta
    
    def __init__(self, parameter_name, parameter_type):
        self._name = parameter_name
        self._type = parameter_type
        self._variables = {}

        self._hidden_variables = {}
        self.__setupHiddenVariables()
        
        self._file = ""
        self._id = 0

    def __setupHiddenVariables(self):

        for name in HIDDEN_VARIABLES:
            self._hidden_variables[name] = 0.0
        
    @abc.abstractmethod
    def applyParameter(self, data):
        pass

    def setVariable(self, name, value):
        self._variables[name] = float(value)

    def setHiddenVariable(self, name, value):
        self._hidden_variables[name] = float(value)

    def setId(self, id):
        self._id = id

    def getId(self):
        return self._id
    
    def getVariable(self, name):
        return self._variables[name]

    def getHiddenVariable(self, name):
        return self._hidden_variables[name]

    def getVariables(self):
        return [i for i in self._variables]

    def getHiddenVariables(self):
        return [i for i in self._hidden_variables]
        
    def getName(self):
        return self._name

    def getType(self):
        return self._type

    def getFile(self):
        return self._file
    
    def setFile(self, parameterfile):
        self._file = parameterfile


class IInteractiveParameter(IParameter):

    __metaclass__ = abc.ABCMeta

    def __init__(self, parameter_name, parameter_type):

        IParameter.__init__(self, parameter_name, parameter_type)

    @abc.abstractmethod
    def applyParameter(self, data):
        pass

    @abc.abstractmethod
    def interaction(self, dataInput, dataNow, dataAudio, parent=None):
        pass
