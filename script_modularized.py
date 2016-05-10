# -*- coding: utf-8 -*-

from struct import pack
from scipy.io import wavfile
from scipy.fftpack import rfft, irfft

import numpy as np

import matplotlib.pyplot as plt

import time
import sys
import posix_ipc
import math
import pyaudio
import wave
import threading
import ConfigParser

#local imports
from animation import *
from window import *

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


# global variables

CHUNK = 1024
CONFIG_FILE = 'config.ini'
DEFAULT_FILTER_FREQUENCY_HZ = 20
MESSAGE_QUEUE_NAME = '/test_queue2'

global audio_file
global message_queue_name
global threads

global audio_rate
global audio_data, filtered_data
global mq

global animation_thread
global run_animation

global window

global configs
global filter_frequency_hz
global parameters_changed

global animationObject

# measures the time of a function call, using decorator @timing
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

def window_rms(signal, window_size):

    #calculates the RMS value for each 'window_size' values of the signal
    signal_squared = np.power(signal,2)
    window = np.ones(window_size)/float(window_size)
    indexes = np.s_[::window_size]
    data = np.sqrt(np.convolve(window, signal_squared, 'valid'))[indexes]

    #low pass filter
    fftdata = rfft(data)
    fftdata[int(filter_frequency_hz*np.pi*2):] = 0

    ##removes negative values
    filtered_data = irfft(fftdata).clip(0)

    return data, filtered_data


def generateAnimation(data, data_frame):

    #splits the data in 2 arrays (left and right channel)
    #data_left = [..] * 
    data_left = np.squeeze(np.asarray(data[44:] * np.matrix('1;0')))
    data_right = np.squeeze(np.asarray(data[44:] * np.matrix('0;1')))

    #no need for 0.5 multiplication: values are scaled later
    #data_mono = 0.5 * (data_right + data_left)
    data_mono = (data_right + data_left)
    
    t, filtered_data = window_rms(data_left, data_frame)
    t = t/t.max()
    filtered_data = filtered_data/filtered_data.max()

    return t, filtered_data
    
def playAudio(file):

    global mq, animation_data, run_animation
    
    wf = wave.open(file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    
    
    #read data (based on the chunk size)
    data = wf.readframes(CHUNK)

    animationObject.startAnimationSignal()
    
    # play stream (looping from beginning of file to the end)
    while (data != ''):
        # writing to the stream is what *actually* plays the sound.
        if (animationObject.running == False):
            break
            
        stream.write(data)
        data = wf.readframes(CHUNK)
        
    stream.close()
    p.terminate()


def reloadAnimation():

    global filter_frequency_hz
    filter_frequency_hz = int(window.lpffrequency.value())

    loadAudioFile()
    
def loadAudioFile():

    global audio_rate, audio_data, animation_data, filtered_data

    if (audio_file != ''):
        audio_rate, audio_data = wavfile.read(audio_file)

        total_time = float(len(audio_data))/ (audio_rate*60)
        string_time = str(int(math.floor(total_time))) + ":" + str((len(audio_data)/audio_rate) % 60)
        data_frame = audio_rate / 60.0
        data_size = len(audio_data) / int(data_frame)

        animation_data, filtered_data = generateAnimation(audio_data[4096:], data_frame)
        animationObject.setAnimationData(filtered_data*2 - 1)
        
        parameters_changed = False

        parametersChangedButtons(parameters_changed)
        window.startanimation.setEnabled(True)
        #buttonStatusWhileExecution(True)
        
    else:
        total_time = "-"
        string_time = "-"
        data_frame = 0
        data_size = "-"

        animation_data = np.array([])
        animationObject.setAnimationData(np.array([]))
 
        buttonStatusWhileExecution(False)
        window.startanimation.setEnabled(False)
        window.selectfile.setEnabled(True)
        window.reloadanimation.setEnabled(False)
        
    window.duration.setText("Sound duration: " + string_time)
    window.animationsizelabel.setText("Animation data size: " + str(data_size))
    
def selectFile():

    global audio_file
    
    audio_file = str(QtGui.QFileDialog.getOpenFileName())
    window.wavfile.setText(audio_file)

    reloadAnimation()


def plotAnimationExec():

    plt.plot(animation_data)
    plt.plot(animationObject.getAnimationData())
    plt.show()
    
    
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

        
def lpfFrequencyChanged():

    parameters_changed = not (window.lpffrequency.value() == filter_frequency_hz)
    parametersChangedButtons(parameters_changed)

def parametersChangedButtons(value):

    window.startanimation.setEnabled(not value)
    window.plotamplitude.setEnabled(not value)
    window.clearanimation.setEnabled(not value)

    if (animation_data.size > 0):
        window.reloadanimation.setEnabled(value)

def callAnimationStart():
    animationObject.startAnimation(onAnimationStart, onAnimationAction, onAnimationFinish)
    
def onAnimationStart():
    window.startanimation.setText("Stop animation")
    buttonStatusWhileExecution(False)
    threads.append(animationObject.thread)

def onAnimationAction():
    playAudio(audio_file)
    
def onAnimationFinish():
    window.startanimation.setText("Start animation")
    buttonStatusWhileExecution(True)
    
#set initial variables
        
audio_file = ''
message_queue_name = MESSAGE_QUEUE_NAME
audio_rate = 0
audio_data = np.array([])
filtered_data = np.array([])
animation_data = np.array([])

threads = []

filter_frequency_hz = DEFAULT_FILTER_FREQUENCY_HZ
parameters_changed = False

animationObject = Animation()
animationObject.setQueueName(message_queue_name)

#loads config file

configs = ConfigParser.ConfigParser()
app, window = windowStart()

window.setFixedSize(window.geometry().width(), window.geometry().height())

buttonStatusWhileExecution(False)

window.startanimation.setEnabled(False)
window.selectfile.setEnabled(True)
window.lpffrequency.setEnabled(True)

window.setWindowTitle("OpenGL Spheres Controller")

try:
    configs.read(CONFIG_FILE)
    
    filter_frequency_hz = configs.getint('General', 'filter_frequency_hz')
    window.lpffrequency.setValue(filter_frequency_hz)
    
    audio_file = str(configs.get('General', 'audio_file'))
    window.wavfile.setText(audio_file)

    window.statusbar.showMessage("Config file loaded!")
    
except:
    window.statusbar.showMessage("Could not load config file!")


reloadAnimation()

window.selectfile.clicked.connect(selectFile)

window.startanimation.clicked.connect(callAnimationStart)
window.plotamplitude.clicked.connect(plotAnimation)
window.clearanimation.clicked.connect(animationObject.clearAnimationSignal)

window.lpffrequency.valueChanged.connect(lpfFrequencyChanged)
window.reloadanimation.clicked.connect(reloadAnimation)
window.actionEdit.triggered.connect(window.openParametersDialog)

app.exec_()

threads = 0

configs.set('General', 'audio_file', audio_file)
configs.set('General', 'filter_frequency_hz', filter_frequency_hz)

file_handle = open(CONFIG_FILE, 'w')
configs.write(file_handle)

sys.exit()
