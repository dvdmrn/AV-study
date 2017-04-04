import abc
import parameters

import numpy as np

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
    
SignalErrors = enum('FILE_EMPTY', 'FILE_NOT_FOUND', 'INVALID_EXTENSION', 'INVALID_FORMAT', 'INVALID_PARAMETER')

class SignalException(Exception):
    def __init__(self, code, message=""):
        self.args = (code, message)
        
class Signal():

    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        self._resetVars()

    def _resetVars(self):
        self._data = np.array([])
        self._animation_data = np.array([])
        self.clearParameters()
        
    def addParameter(self, parameter):
        """
        Adds a processing step to the signal.
        """
        
        if (isinstance(parameter, parameters.IParameter)):
            self._parameters.append(parameter)
        else:
            raise SignalException(SignalErrors.INVALID_PARAMETER, "The parameter must inherit from IParameter class!")

    def getParameters(self):
        return self._parameters

    def copyHiddenVariables(self, fromparameter, toparameter):
        for ind in fromparameter.getHiddenVariables():
            toparameter.setHiddenVariable(ind, fromparameter.getHiddenVariable(ind))

    def applyParameters(self):
        """
        Processes the signal through all the parameters previously added
        """
        fromparameter = None
        
        for parameter in self._parameters:
            print "Applying: ", parameter.getName()
            if (fromparameter != None):
                self.copyHiddenVariables(fromparameter, parameter)
                
            self._animation_data = parameter.applyParameter(self._animation_data)
            fromparameter = parameter
            
    def clearParameters(self):
        self._parameters = []

    def addOffset(self, offset):
        """
        Adds an offset to the animation data.
        Must be called after the generation of the animation, otherwise won't affect the results.
        """
        self._animation_data.__iadd__(offset)

    def generateAnimation(self):
        self._animation_data = np.array([])

    def getAnimationData(self):
        return self._animation_data

    def getData(self):
        return self._data

    def clearData(self):
        self._resetVars()
