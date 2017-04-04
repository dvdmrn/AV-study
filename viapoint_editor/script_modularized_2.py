# -*- coding: utf-8 -*-

import numpy as np

import matplotlib.pyplot as plt

import time
import sys
import math
import threading
import ConfigParser

#local imports
from animation import *
from window import *
from parameters import *
from signals import *
from wavsignal import *
from hdfsignal import *
from lpf import *

#from PyQt4 import *
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *



# global variables

CONFIG_FILE = 'config.ini'
DEFAULT_FILTER_FREQUENCY_HZ = 20
MESSAGE_QUEUE_NAME = '/test_queue2'

ANIMATION_TYPE_NONE = 0
ANIMATION_TYPE_WAV_FILE = 1
ANIMATION_TYPE_HDF_FILE = 2

global audio_file, hdf_file
global threads

global window

global configs
global filter_frequency_hz
global parameters_changed

global animationObject
global lpf
global wavsignal
global hdfsignal

global animationType
global hdf_branch

# measures the time of a function call, using decorator @timing
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap


def reloadAnimation():

    global filter_frequency_hz, hdf_file

    valid = False
    
    if (audio_file != ''):
        
        window.startanimation.setEnabled(True)
        window.plotamplitude.setEnabled(True)
        window.clearanimation.setEnabled(True)
        window.reloadanimation.setEnabled(True)
        
        if (animationType == ANIMATION_TYPE_WAV_FILE):
            
            filter_frequency_hz = int(window.lpffrequency.value())
            lpf.setVariable("FREQUENCY", filter_frequency_hz)

            hdf_file = ''
            loadAudioFile()
            
        elif (animationType == ANIMATION_TYPE_HDF_FILE):

            if (hdf_file == ''):
                while (not valid):
                    try:
                        selectHDFFile()
                        if (hdf_file != ''):
                            loadHDFFile()
                            #selectDatasetNode()
                        valid = True
                    except:
                        valid = False
            else:
                loadHDFFile()
                    
                
            if (hdf_file == ''):
                window.startanimation.setEnabled(False)
                window.plotamplitude.setEnabled(False)
                window.clearanimation.setEnabled(False)
                
            
        else: #animationType == ANIMATION_TYPE_NONE
            hdf_file = ''
            window.startanimation.setEnabled(False)
            window.plotamplitude.setEnabled(False)
            window.clearanimation.setEnabled(False)

    else:
        
        animationObject.setAnimationData(np.array([]))
        wavsignal.clearData()
 
        buttonStatusWhileExecution(False)
        window.startanimation.setEnabled(False)
        window.selectfile.setEnabled(True)
        window.reloadanimation.setEnabled(False)

    window.duration.setText("Sound duration: " + str(wavsignal.getTimeString()))
    window.animationsizelabel.setText("Animation data size: " + str(len(wavsignal.getAnimationData())))
        
def loadHDFFile():
    
    hdfsignal.setFile(hdf_file)
    hdfsignal.loadFile()
    
    if (hdf_branch == ''):
        selectDatasetNode()
    else:
        hdfsignal.setAnimationBranch(hdf_branch)
        
    hdfsignal.loadData()
    
    hdfsignal.generateAnimation()
    hdfsignal.addOffset(-1 - hdfsignal.getAnimationData().min())

    animationObject.setAnimationData(hdfsignal.getAnimationData())
    animationObject.setFPS(hdfsignal.getFPS())

    
def loadAudioFile():

    wavsignal.setFile(audio_file)
    wavsignal.loadFile()
    wavsignal.addParameter(lpf)
    wavsignal.generateAnimation()
    wavsignal.addOffset(-1)
        
    animationObject.setAnimationData(wavsignal.getAnimationData())
    animationObject.setFPS(60.0)


def animationTypeSelect():

    global animationType, hdf_branch
    
    if (window.form_animation_choice.wavType.isChecked()):
        animationType = ANIMATION_TYPE_WAV_FILE
    elif (window.form_animation_choice.hdfType.isChecked()):
        animationType = ANIMATION_TYPE_HDF_FILE
        hdf_branch = ""
    else:
        animationType = ANIMATION_TYPE_NONE

    reloadAnimation()
    
def selectFile():

    global audio_file
    
    audio_file = str(QtGui.QFileDialog.getOpenFileName())
    window.wavfile.setText(audio_file)

    animationType = ANIMATION_TYPE_WAV_FILE

    #window.form_animation_choice.accepted.connect(animationTypeSelect)
    if (audio_file != ''):
        window.openAnimationChoiceDialog()
    else:
        animationType = ANIMATION_TYPE_NONE
        reloadAnimation()

def selectHDFFile():

    global hdf_file
    
    hdf_file = str(QtGui.QFileDialog.getOpenFileName())

def selectDatasetNode():

    window.form_dataset.datalist.clear()
    nodes = hdfsignal.getHDFFile().walkNodes("/", "Array")
    selectedItem = ''
    items = False
    
    for node in nodes:
        window.form_dataset.datalist.addItem(node._v_pathname)
        items = True

    if (not items):
        raise Exception("HDF File must contain at least one dataset!")
        
    window.form_dataset.exec_()

def selectDatasetAccept():
    
    hdf_branch = ""
    
    while (hdf_branch == ''):
        hdf_branch = window.form_dataset.datalist.currentItem().text()

    hdfsignal.setAnimationBranch(hdf_branch)


def plotAnimationExec():

    #plt.plot(wavsignal.getData())
    fig = plt.figure(1)
    plt.plot(animationObject.getAnimationData())
    plt.show()
    plt.close(fig)
    
def plotAnimation():

    if (animationObject.getAnimationData().size > 0):
        
        t = threading.Thread(target=plotAnimationExec)
        threads.append(t)
        t.start()


def buttonStatusWhileExecution(status):

    global window
    
    window.selectfile.setEnabled(status)
    window.clearanimation.setEnabled(status)
    window.plotamplitude.setEnabled(status)
    window.lpffrequency.setEnabled(status)

        
def parametersChangedButtons(value):

    window.startanimation.setEnabled(not value)
    window.plotamplitude.setEnabled(not value)
    window.clearanimation.setEnabled(not value)

    if (wavsignal.getData().size > 0):
        window.reloadanimation.setEnabled(value)

def callAnimationStart():
    animationObject.startAnimation(onAnimationStart, onAnimationAction, onAnimationFinish)
    
def onAnimationStart():
    window.startanimation.setText("Stop animation")
    buttonStatusWhileExecution(False)
    threads.append(animationObject.thread)

def onAnimationAction():
    animationObject.setAudioFile(audio_file)
    animationObject.playAudio()
    
def onAnimationFinish():
    window.startanimation.setText("Start animation")
    buttonStatusWhileExecution(True)

def clearVariables():

    global audio_file, hdf_file
    
    wavsignal.clearData()
    hdfsignal.clearData()
    animationObject.setAnimationData(np.array([]))
    
    audio_file = ''
    hdf_file = ''

    hdf_branch = ''

    window.wavfile.setText("")

    buttonStatusWhileExecution(False)
    window.selectfile.setEnabled(True)
    

    
###################################################################
########################### MAIN PROGRAM ##########################
###################################################################


#########################
# set initial variables #
#########################

animationType = ANIMATION_TYPE_NONE
filter_frequency_hz = DEFAULT_FILTER_FREQUENCY_HZ

threads = []

parameters_changed = False

animationObject = Animation()
animationObject.setQueueName(MESSAGE_QUEUE_NAME)

lpf = LPFParameter()
wavsignal = WavSignal()
hdfsignal = HDFSignal()


##########################
# configures main window #
##########################

app, window = windowStart()

window.setFixedSize(window.geometry().width(), window.geometry().height())

buttonStatusWhileExecution(False)

window.startanimation.setEnabled(False)
window.selectfile.setEnabled(True)
window.lpffrequency.setEnabled(True)

window.setWindowTitle("OpenGL Spheres Controller")

window.selectfile.clicked.connect(selectFile)

window.startanimation.clicked.connect(callAnimationStart)
window.plotamplitude.clicked.connect(plotAnimation)
window.clearanimation.clicked.connect(animationObject.clearAnimationSignal)

window.reloadanimation.clicked.connect(window.openAnimationChoiceDialog)
window.actionEdit.triggered.connect(window.openParametersDialog)

window.form_animation_choice.accepted.connect(animationTypeSelect)
window.form_animation_choice.rejected.connect(clearVariables)

window.form_dataset.accepted.connect(selectDatasetAccept)
#window.form_dataset.rejected.connect(selectDatasetReject)

#######################
# loads configuration #
#######################

clearVariables()

configs = ConfigParser.ConfigParser()

try:
    configs.read(CONFIG_FILE)
    
    filter_frequency_hz = configs.getint('General', 'filter_frequency_hz')
    animationType = configs.getint('General', 'animation_type')
    audio_file = str(configs.get('General', 'audio_file'))
    hdf_file = str(configs.get('General', 'hdf_file'))
    hdf_branch = str(configs.get('General', 'hdf_branch'))
    
    window.statusbar.showMessage("Config file loaded!")
    
except:
    window.statusbar.showMessage("Could not load config file!")


print "Animation type: ", animationType


    
########################
# extra configurations #
########################

window.lpffrequency.setValue(filter_frequency_hz)
lpf.setVariable("FREQUENCY", filter_frequency_hz)

window.wavfile.setText(audio_file)

#animationTypeSelect()
reloadAnimation()


#####################
# opens main window #
#####################

app.exec_()



threads = []

configs.set('General', 'audio_file', audio_file)
configs.set('General', 'hdf_file', hdf_file)
configs.set('General', 'filter_frequency_hz', filter_frequency_hz)
configs.set('General', 'animation_type', animationType)
configs.set('General', 'hdf_branch', hdf_branch)

file_handle = open(CONFIG_FILE, 'w')
configs.write(file_handle)

sys.exit()
