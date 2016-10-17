# -*- coding: utf-8 -*-

import numpy as np
from multiprocessing import Process

import time
import sys
import posix_ipc
import threading
import pyaudio
import wave

import scikits.audiolab

from struct import pack
from scipy.io import wavfile
from scipy.fftpack import rfft, irfft

DEFAULT_FRAME_RATE = 60.0
CHUNK = 1024

class Animation():
    
    def __init__(self):
        
        self.mq = -1
        self.animation_data = np.array([])
        self.running = False
        self.thread = threading.Thread()
        self.__queue_name = ""
        self.data_frame = DEFAULT_FRAME_RATE
        self.__audio_file = ""
        self._audio_data = np.array([])
        self._rate = 44100

        self.__onStart = None
        self.__onAction = None
        self.__onFinish = None

    def isRunning(self):
        return self.running
    
    def setQueueName(self, queuename):
        self.mq = -1
        self.__queue_name = queuename
        
    def connectToQueue(self):
        if (self.mq != -1):
            return True
        
        try:
            self.mq = posix_ipc.MessageQueue(self.__queue_name, 0)
        except Exception as e:
            print e
            
        if (self.mq == -1):
            return False
        else:
            return True

    def __startAnimationExec(self):
        if (self.connectToQueue()):
            self.sendAnimationData()
            if (not (self.__onAction is None)):
                
                self.__onAction()
        self.running = False
        if (not (self.__onFinish is None)): self.__onFinish()

    def startAnimation(self, onStart, onAction, onFinish):
        
        if (not self.thread.isAlive()):
            if (self.animation_data.size > 0):
                self.running = True
                self.__onStart = onStart
                self.__onAction = onAction
                self.__onFinish = onFinish
                
                self.thread = threading.Thread(target=self.__startAnimationExec)
                if (not (self.__onStart is None)): self.__onStart()
                self.thread.start()
        else:
            self.stopAnimationSignal()
            self.running = False

    def stopAnimation(self):
        if (self.thread.isAlive()):
            self.running = False
            self.stopAnimationSignal()
            #if (not (self.__onFinish is None)): self.__onFinish()
    
    def setAnimationData(self, animationdata):
        self.animation_data = animationdata

    def getAnimationData(self):
        return self.animation_data

    def sendAnimationData(self):
        self.stopAnimationSignal()
        self.clearAnimationSignal()
        self.sendFPSSignal()
            
        for i in self.animation_data:
            self.sendMessage('p', 0.0, i, 0.0)
        
    def sendMessage(self, c, x=0.0, y=0.0, z=0.0):
        if (self.connectToQueue()):
            self.mq.send(pack('fffc', float(x), float(y), float(z), str(c)))
            
    def clearAnimationSignal(self):
        self.sendMessage('c')

    def stopAnimationSignal(self):
        self.sendMessage('x')

    def startAnimationSignal(self):
        self.sendMessage('s')

    def setFPS(self, fps):
        self.data_frame = float(fps)

    def getFPS(self):
        return self.data_frame
    
    def sendFPSSignal(self):
        self.sendMessage('f', x=self.data_frame)

    def setAudioFile(self, audio_file):
        self.__audio_file = audio_file

    def setAudioData(self, audio_data):
        self._audio_data = audio_data

    def setAudioRate(self, rate):
        self._rate = rate

    def getAudioRate(self):
        return self._rate
    
    def getAudioData(self):
        return self._audio_data

    def playAudio(self):
        if (self.__audio_file != ""):
            print "Playing audio:", self.__audio_file
            wf = wave.open(self.__audio_file, 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    
    
            #read data (based on the chunk size)
            data = wf.readframes(CHUNK)

            self.startAnimationSignal()
    
            # play stream (looping from beginning of file to the end)
            while (data != ''):
                # writing to the stream is what *actually* plays the sound.
                if (self.running == False):
                    break
            
                stream.write(data)
                data = wf.readframes(CHUNK)
        
            stream.close()
            p.terminate()

    def __playingAction(self):
        scikits.audiolab.play(self._audio_data, self._rate)
        self.running = False

    def playAudio2(self):
        
        self.running = False
        
        if (self.__audio_file != ""):
            if (self._audio_data.size > 0):
                
                p = Process(target=self.__playingAction)
                self.running = True
                
                self.startAnimationSignal()
                p.start()

                while (not p.is_alive()):
                    pass
                
                while (p.is_alive()):
                    if (not self.running):
                        p.terminate()
                        break
                    
                self.running = False
