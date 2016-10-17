# -*- coding: utf-8 -*-

import os
import sys
import glob
import ntpath

from mainwindow import *
from mainwindowold import *
from parametersdialog import *
from AnimationChoice import *
from DatasetDialog import *

from animationlist import *

from chooselist import *
from animationselectiondialog import *

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def windowStartOld():
    
    app = QtGui.QApplication(sys.argv)    
    window = WindowMain()
    
    window.show()

    return (app, window)


class AnimationChoice(QDialog, Ui_AnimationDialog):
    def __init__(self):
        QDialog.__init__(self)

        self.setupUi(self)

class ParametersDialog(QDialog, Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)

        self.setupUi(self)

class DatasetDialog(QDialog, Ui_DatasetDialog):
    def __init__(self):
        QDialog.__init__(self)

        self.setupUi(self)
    
class WindowMain(QMainWindow, Ui_MainWindowOld):
    def __init__(self):
        QMainWindow.__init__(self)

        self.form_parameters = ParametersDialog()
        self.form_animation_choice = AnimationChoice()
        self.form_dataset = DatasetDialog()
        
        self.setupUi(self)

    def openParametersDialog(self, arg2):
        self.form_parameters.show()

    def openAnimationChoiceDialog(self):
        self.form_animation_choice.exec_()

    def openDatasetDialog(self):
        self.form_dataset.exec_()
