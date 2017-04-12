# ----------------------------------------------------------------
# Run this script by typing:
#	python ballHDF.py <HDF_file_path> <sound_file_path>
# Note: sounds must be a wav file!
# ----------------------------------------------------------------


import pygame
from pygame import gfxdraw
from pygame import mixer
from math import pi
from numpy import interp

import scipy.io.wavfile as wavfile
import numpy as np
import pylab

import time
import random
import collections
import csv
import tables
import string

import sys

from tables import *


#HDFfilepath = sys.argv[1]

# soundFilePath = sys.argv[2]

# print('sound path')
# print(soundFilePath)
# sound path

import glob, os
import os.path

from os import listdir
from os.path import isfile, join

from os import listdir
from os.path import isfile, join

# gets current working directory, place where it is ran
current_dir = os.getcwd()
#print ("current dir: ",current_dir)

trial = 1
trialIndex = 0
soundFilePath = ""

numBlanksToAdd = 10
numOfRepeatedSoundFiles = 0

# TODO generates list for HDF files
hdf_dir = '../data/trials/hdfConditions/'
#hdf_dirs = sorted(os.listdir( hdf_dir ))
sorted_hdf_dirs = sorted(os.listdir( hdf_dir ))

print('\n')
#print('sorted hdf_dirs ', sorted_hdf_dirs)


hdf_dirs = os.listdir( hdf_dir )
#print('hdf_dirs ', hdf_dirs)

print("Sorted Files in HDF")
# This would print all the files and directories
for file in sorted_hdf_dirs:
   print file



print('\n')
numOfRepeatedSoundFiles = int(raw_input("Please enter the number of time to repeat sound files: "))
print "Number of time to repeat sound files is set as: ", numOfRepeatedSoundFiles


# TODO generates list for sound WAV files
wav_dir = '../data/trials/wavConditions/'
#wav_dirs = sorted(os.listdir( wav_dir ))

sorted_wav_dirs = []
print("make sure sorted wav list is reset: ", sorted_wav_dirs)


wav_dirs = os.listdir( wav_dir )
print('wav_dirs ', wav_dirs)
sorted_wav_dirs = sorted(os.listdir( wav_dir ))

for n in range(numOfRepeatedSoundFiles-1):
    for i in range(len(wav_dirs)):
        sorted_wav_dirs.append(wav_dirs[i])


# resort the list
sorted_wav_dirs = sorted(sorted_wav_dirs)

#print('sorted_wav_dirs', sorted_wav_dirs)
print('\n')


print("Files in sorted wav")
# This would print all the files and directories
for file in sorted_wav_dirs:
   print file
print('\n')


# Find the directory with the fewest amount of files to determine how many trials to run
# assuming one file per trial
shortest_list = 0
if len(sorted_hdf_dirs) < len(sorted_wav_dirs):
    shortest_list = len(sorted_hdf_dirs)
else:
    shortest_list = len(sorted_wav_dirs)
print('Fewest number of files, shortest list: ',shortest_list)
print ('/n')


print('\n')
pid = raw_input("Please enter the participant id: ")
print "PID is set as: ", pid


# ----------------------------------------------------------------
#      pytables
# ----------------------------------------------------------------

class Animation(IsDescription):
    frame = Float64Col()


HDFfilepath = sorted_hdf_dirs[trialIndex]
print('hdffilepath :', sorted_hdf_dirs[trialIndex])

# opens h5file
# !!!
# prints two lists, one for the hdf file, another for hdf files in the folder
for root, dirs, files in os.walk(hdf_dir):
    print "get the files", files

HDFfilepath = os.path.join(hdf_dir, sorted_hdf_dirs[trialIndex])
h5file = open_file(HDFfilepath, mode="r+", title="Trial file")

# attempt at adding blank rows in existing HDF file
'''
class HDFContents(IsDescription):
    numRows      = Int32Col()       # 32-bit integer
    animValue    = Float32Col()    # float  (single-precision

group = h5file.create_group("/", 'detector', 'Detector information')
newRows = h5file.create_group(h5file.root, "rows", "frames")
newTable = h5file.create_table(group, 'readout', HDFContents, "Offset HDF file")
hdfContents = newTable.row
# go to the next row (numRows) then add a 0 to offset the HDF animation
for i in xrange(numBlanksToAdd):
    hdfContents['numRows'] = i
    hdfContents['animValue'] = 0
    # Insert a new HDFContents row record
    hdfContents.append()
# maintain integrirty of file and free up memory reosources
newTable.flush()
newTable = h5file.root.detector.readout
'''

table = h5file.root.animation
# constructs array of frame vals
# !!! min max values can be found in here \/ below
frames = [x for x in table.iterrows()]
# print("show frames", frames)
# print("max", max(frames))
# print("min", min(frames))


# will be used to interate frames in main loop
frameIndex = 0
frameRate = 0

# ----------------------------------------------------------------
#      keylog setup
# ----------------------------------------------------------------

keylogData = collections.OrderedDict()
keylogFrameData = collections.OrderedDict()
# ----------------------------------------------------------------
#      pygame setup
# ----------------------------------------------------------------


# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# circle position
xPos = 0
yPos = 0
# window params
height = 480
width = 700 #640
radius = 40;

# Gap between the edge of the screen and where the ball can reach
# Prevents the ball from going off screen or touching the edge of the screen
borderGap = 12;

ballColor = BLUE
# Set the width and height of the screen
size = [width, height]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("AV Welcome Screen")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

# Multiple screen variables
FPS = 15


smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (width / 2), (height / 2) + y_displace
    screen.blit(textSurf, textRect)


def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(WHITE)
        message_to_screen("Welcome to the AV Study",
                          BLUE,
                          -100,
                          "large")
        message_to_screen("Instructions: Please press the space bar to match with each ball bounce",
                          BLACK,
                          -10)

        message_to_screen("Press C to start",
                          BLACK,
                          70)

        pygame.display.update()
        #clock.tick(FPS)
        clock.tick(frameRate)

def trialLoop():
    global trial
    global HDFfilepath
    global soundFilePath
    global h5file
    global table
    global frames
    global done
    global frameIndex
    global trialIndex
    global keylogData
    global keylogFrameData

   # trial += 1
    gameExit = False
    gameOver = False
    trialMessage = "Trial " + str(trial) + " is over"

    print("Current Trial: ",str(trial))

    # count from 0 to length of list - 1 , since range is 0 to 1 before shortest_list

    # HDFfilepath = hdf_dirs[0]
    file = sorted_hdf_dirs[trialIndex]
    print 'hdf name :', sorted_hdf_dirs[trialIndex]

    #HDFfilepath = os.path.abspath(file)
    #print ('hdf_path2', os.path.abspath(file))

    HDFfilepath = os.path.join(hdf_dir, sorted_hdf_dirs[trialIndex])
    print 'Current hdf_path: ', HDFfilepath

    #todo is this the issue?
    h5file = open_file(HDFfilepath, mode="r+", title="Test file")
    table = h5file.root.animation
    #print("loop table", table)

    # wav file path
    soundfile = sorted_wav_dirs[trialIndex]

    soundFilePath = os.path.join(wav_dir, sorted_wav_dirs[trialIndex])
    print('\n')
    print('IN TRIAL ', trial, 'sound file :', sorted_wav_dirs[trialIndex])
    # print('Current soundfile name :', sorted_wav_dirs[trialIndex])
    #print(soundfile)


    # constructs array of frame vals
    # !!! min max values can be found in here \/ below
    frames = [x for x in table.iterrows()]
    done = False
    frameIndex = 0
    ball()

    start_ticks = pygame.time.get_ticks()  # starter tick

    hasExported = False # by default, the csv file has not been exported
    # print "Number of trial indexes to run %d" % (x)

    if trial == shortest_list:
        if hasExported == False:  # This ensures the .csv file is only written once
            hasExported = True
            print('\n')
            print(trialMessage)
            exportVals(keylogData, keylogFrameData)

    trial += 1

    if trial > shortest_list:
        gameEnd()

    trialIndex += 1

    while not gameExit:

        while gameOver == False:

            numSecondsToWait = 7  #number of seconds to wait before going to the next trial
            seconds = (pygame.time.get_ticks() - start_ticks) / (numSecondsToWait* 100)  # calculate how many seconds
            countdownSeconds = numSecondsToWait-seconds
            if seconds > numSecondsToWait:  # if more than numSecondsToWait seconds go to the next trial
                trialLoop()
                gameEnd()
            if hasExported == False:  #This ensures the .csv file is only written once
                hasExported = True
                print('\n')
                print(trialMessage)
                exportVals(keylogData,keylogFrameData)


            countdownMessage = "Next trial is in  " + str(countdownSeconds) + " seconds."
            #print("count down Message: ", countdownMessage)


            screen.fill(WHITE)
            message_to_screen(trialMessage,
                              RED,
                              y_displace=-40,
                              size="large")

            message_to_screen(countdownMessage,
                              BLACK,
                              50,
                              size="medium")

            '''message_to_screen("Please take a break.",
                              BLACK,
                              50,
                              size="medium")
            '''

            message_to_screen("Press C to start the next trial",
                              BLACK,
                              120)

            pygame.display.update()


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = True
                        gameEnd()
                    if event.key == pygame.K_c:
                        trialLoop()
                        gameEnd()
                #Export data when done a trial not during since the particpants is using it
                    if event.key == pygame.K_e:
                        exportVals(keylogData,keylogFrameData)

            #clock.tick(FPS)
            clock.tick(frameRate)

    #pygame.quit()
    #quit()


# Draw a circle
#   unfortunately if you want antialiasing support is only available for
#   the outline of a circle, so we must draw the filled circle beneath the outlined
#   circle. :(
def circle(x, y, r, color):
    pygame.gfxdraw.filled_circle(screen, x, y, r, color)
    pygame.gfxdraw.aacircle(screen, x, y, r, color)


def inferFrameRate(frames, soundFilePath):
    a = pygame.mixer.Sound(soundFilePath)
    #print("length of sound file: ", a.get_length())
    #print("number of frames: ", len(frames))
    return (len(frames) / a.get_length())


def ball():
    smoothY = 0
    global frameRate
    global keylogData
    global keylogFrameData

    print('Sound file used: ', soundFilePath)
    frameRate = inferFrameRate(frames, soundFilePath)

    #print("did inferframerate work? ", frameRate)

    # Load audio
    pygame.mixer.music.load(soundFilePath)

    pygame.mixer.music.play(0, 0.0)

    initTime = time.time()
    pressVal = 0

    # ----------------------------------------------------------------
    #      pygame main loop
    # ----------------------------------------------------------------
    global done
    global frameIndex

    #onedeeframes = np.append(np.array([]), np.array([3,1,3,5,3]))
    # for f in xrange(0,len(frames)):
    #     np.append(onedeeframes,frames[f][0])

    #print("before frameposition 0", frames[0])
    #print("before frameposition 2,0", frames[2][0])
    print("min frames", min(frames)[0])
    print("max frames", max(frames)[0])
    # print("frames: ", frames)


    while not done:
        #print("Farm index in while", frameIndex)
        # This sets the framerate
        # Leave this out and we will use all CPU we can.

        #clock.tick_busy_loop(frameRate )
        clock.tick_busy_loop(frameRate - 2)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


        #print onedeeframes
        #print ("min ", min(onedeeframes))
        #print ("max frames", max(onedeeframes))
        #print("Farme dex", frameIndex)

        # interp does what MapRange is supposed to do
        # interp(dataPoint, [from_min,from_max],[to_min,to_max])
        # Rounds and makes frames into integers and translates the range of values in frames into the matching screen dimensionsf
        # radius and borderGap is added to prevent the ball from being displayed to the edges of the screen and avoid displaying only part of the ball
        #framePosition = int(round(interp(onedeeframes[3], [min(onedeeframes), max(onedeeframes)],
        #                                 [0 + radius + borderGap, height - radius - borderGap])))

        # This must be in the while loop to update the frames and animation
        #frames itterate through the list of frames first (find the values in the list of arrays) then obtains the value in this array (index 0)
        framePosition = int(round(interp(frames[frameIndex][0], np.array([min(frames)[0], max(frames)[0]]),
                                        np.array([0 + radius + borderGap, height - radius - borderGap]))))

        '''
        # Use this if you want to switch the peak of the sound to when the ball touches the ground
        # framePosition if numbers were positive * -1 offset, then the biggest value 0.9 becomes the smallest -0.9.
        # counteract the switch, - height from it
        # or ensure HDF frame input are all positive values (no *-1 offset in animation player) to avoid switch
        # check to make sure the max frames are not a negative number, if it's negative, switch, if not stay
        if max(frames)[0] < 0:
            yPos = abs(framePosition - height)
        else:
            yPos = framePosition
        '''

        yPos = abs(framePosition - height)

        if yPos < 0:
            yPos = 0
        # boundary checking
        if yPos > height:
            yPos = height

        # Keep track of yPos
        # print("yPos:", yPos)

        # update time stamp
        currentTime = time.time()
        currentTime = currentTime - initTime
        keylogData[currentTime] = pressVal
        #keylogFrameData[currentTime] = frames[frameIndex][0]
        frameLogging = interp(frames[frameIndex][0], np.array([min(frames)[0], max(frames)[0]]),
                                        np.array([0,1]))
        keylogFrameData[currentTime] = frameLogging


        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
                #gameOver = False
                #gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pressVal = 1
                if event.key == pygame.K_0:
                    print keylogData
                if event.key == pygame.K_f:
                    print keylogFrameData
                #if event.key == pygame.K_e:
                 #   exportVals(keylogData)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                    pressVal = 0

            #clock.tick(FPS)q
            clock.tick(frameRate)

        # Clear the screen and set the screen background
        screen.fill(WHITE)

        smoothY = int(smoothY*0.5+yPos*0.5)
        circle((width / 2), smoothY, radius, ballColor)

        frameIndex += 1
        # Updates screen: this MUST happen after all the other drawing commands.
        pygame.display.flip()

        # make sure Index does not go out of bounds
        if frameIndex == len(frames)-1:
            print("keylogdata :"+str(keylogData.items()[0])+"..."+str(keylogData.items()[20])+"...")
            print("keylogFramedata :" + str(keylogFrameData.items()[0]) + "..." + str(keylogFrameData.items()[20]) + "...")
            gameOver = True
            done = True




def exportVals(klData, klfData):
    global keylogData
    global keylogFrameData
    currentHdfName = sorted_hdf_dirs[trialIndex].split(".")[0]
    currentHdfName = currentHdfName.split('_', 1)[-1]
    currentHdfName = currentHdfName.split(" ")[0]
    print('currentHdfName', currentHdfName)

    # Key Log Data, save in the participant_data folder
    # Record the time and key log responses
    #with open('pid' + pid + '_trial' + str(trial) + '_' + currentHdfName + '.csv', 'w') as csvfile:
    with open('../data/participant_data/' + 'pid' + pid + '_trial' + str(trial-1) + '_' + currentHdfName + '_' + 'keylog' + '.csv', 'wb') as csvfile:
        fieldnames = ['time', 'keypress']
        writer = csv.writer(csvfile)
        # writer.writeheader()
        keylogDataOutput = klData.items()
        print "writing " +  currentHdfName + ".csv"
        for e in keylogDataOutput:
            writer.writerow(e)
        print "finished writing keylog file"
        keylogData = collections.OrderedDict()
        print('\n')

    # Record the same time and frame rate for the trial
    with open('../data/participant_data/' + 'pid' + pid + '_trial' + str(trial-1) + '_' + currentHdfName + '_' + 'frames' + '.csv','wb') as csvframefile:
        fieldnames2 = ['time', 'frames']
        writer = csv.writer(csvframefile)
        # writer.writeheader()
        keylogFrameDataOutput = klfData.items()
        print "writing " + currentHdfName + ".csv"
        for e in keylogFrameDataOutput:
            writer.writerow(e)
        print "finished writing frame file"
        keylogFrameData = collections.OrderedDict()
        print('\n')


def gameEnd():
    end = True
    global trial

    while end:
        screen.fill(WHITE)
        message_to_screen("Thank you for completing the experiment",
                          BLUE,
                          -100,
                          "medium")
        message_to_screen("Please notify the experimenter",
                          BLACK,
                          -10)

        message_to_screen("Close the window or press Q to quit.",
                          BLACK,
                          70)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        pygame.display.update()
        #clock.tick(FPS)
        clock.tick(frameRate)


game_intro()
trialLoop()
gameEnd()

# Be IDLE friendly
pygame.quit()