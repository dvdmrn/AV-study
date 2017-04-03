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
import numpy
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
print ("current dir:",current_dir)

trial = 0
trialIndex = 0
soundFilePath = ""

numBlanksToAdd = 10

# TODO works with HDF Dir
hdf_dir = '../data/trials/hdfConditions/'
#hdf_dirs = sorted(os.listdir( hdf_dir ))
sorted_hdf_dirs = sorted(os.listdir( hdf_dir ))


print('sorted hdf_dirs ', sorted_hdf_dirs)

print('0 HDF', sorted_hdf_dirs[0])
print('1 HDF' , sorted_hdf_dirs[1])
print('2 HDF', sorted_hdf_dirs[2])
print('\n')


hdf_dirs = os.listdir( hdf_dir )
print('hdf_dirs ', hdf_dirs)
print('hdf_dir ', hdf_dir)

print("Files in HDF")
# This would print all the files and directories
for file in hdf_dirs:
   print file
   #print os.path.abspath(file)
   #print('combine the paths: ', hdf_dir+file)

print('0 HDF', hdf_dirs[0])
print('1 HDF' , hdf_dirs[1])
print('2 HDF', hdf_dirs[2])
print('\n')


# TODO for sound WAV
wav_dir = '../data/trials/wavConditions/'
#wav_dirs = sorted(os.listdir( wav_dir ))
wav_dirs = os.listdir( wav_dir )
print('wav_dirs ', wav_dirs)
sorted_wav_dirs = sorted(os.listdir( wav_dir ))
print('sorted_wav_dirs', sorted_wav_dirs)


print('0 WAV' , sorted_wav_dirs[0])
print('1 WAV' , sorted_wav_dirs[1])
print('2 WAV', sorted_wav_dirs[2])
print('\n')


print("Files in wav")
# This would print all the files and directories
for file in wav_dirs:
   print file
print('0 WAV' , wav_dirs[0])
print('1 WAV' , wav_dirs[1])
print('2 WAV', wav_dirs[2])
print('\n')

# Find the directory with the fewest amount of files to determine how many trials to run
# assuming one file per trial
shortest_list = 0
if len(sorted_hdf_dirs) < len(sorted_wav_dirs):
    shortest_list = len(sorted_hdf_dirs)
else:
    shortest_list = len(sorted_wav_dirs)
print('fewest number of files:',shortest_list)

# ----------------------------------------------------------------
#      pytables
# ----------------------------------------------------------------

class Animation(IsDescription):
    frame = Float64Col()


HDFfilepath = sorted_hdf_dirs[trial]
print('hdffilepath :', sorted_hdf_dirs[trial])

# opens h5file
# !!!
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
print("max", max(frames))
print("min", min(frames))

# will be used to interate frames in main loop
frameIndex = 0
frameRate = 0

# ----------------------------------------------------------------
#      keylog setup
# ----------------------------------------------------------------

keylogData = collections.OrderedDict()

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

print("height", height)
print("width", width)

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


pid = raw_input("Please enter the participant id: ")
print "PID is set as: ", pid

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

   # trial += 1
    gameExit = False
    gameOver = False
    trialMessage = "Trial " + str(trial+1) + " is over"
    print("trialMessage: ", trialMessage)

    print("game exit", gameExit)
    print("trial in loop",str(trial))

    # count from 0 to length of list - 1 , since range is 0 to 1 before shortest_list
    for x in range(0, shortest_list):
        print "Number of trial indexes to run %d" % (x)
        trial += 1

        if trial > shortest_list:
            gameEnd()

        # HDFfilepath = hdf_dirs[0]
        file = sorted_hdf_dirs[trialIndex]
        print('hdf name :', sorted_hdf_dirs[trialIndex])

        #HDFfilepath = os.path.abspath(file)
        #print ('hdf_path2', os.path.abspath(file))

        HDFfilepath = os.path.join(hdf_dir, sorted_hdf_dirs[trialIndex])
        print ('current hdf_path: ', HDFfilepath)


        h5file = open_file(HDFfilepath, mode="r+", title="Test file")
        table = h5file.root.animation

        # wav file path
        soundfile = sorted_wav_dirs[trialIndex]

        soundFilePath = os.path.join(wav_dir, sorted_wav_dirs[trialIndex])
        print('\n')
        print('in trial', trial, 'sound path :', soundFilePath)
        print('soundfile name :', sorted_wav_dirs[trialIndex])
        #print(soundfile)
        print('\n')

        trialIndex += 1
        # constructs array of frame vals
        # !!! min max values can be found in here \/ below
        frames = [x for x in table.iterrows()]
        done = False
        frameIndex = 0
        ball()

        start_ticks = pygame.time.get_ticks()  # starter tick

        hasExported = False # by default, the csv file has not been exported

        while not gameExit:

            while gameOver == False:

                numSecondsToWait = 10  #number of seconds to wait before going to the next trial
                seconds = (pygame.time.get_ticks() - start_ticks) / (numSecondsToWait* 100)  # calculate how many seconds
                countdownSeconds = numSecondsToWait-seconds
                if seconds > numSecondsToWait:  # if more than numSecondsToWait seconds go to the next trial
                    trialLoop()
                    gameEnd()
                if hasExported == False:  #This ensures the .csv file is only written once
                    hasExported = True
                    exportVals(keylogData)


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
                            exportVals(keylogData)

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
    print("length of sound file: ", a.get_length())
    print("number of frames: ", len(frames))
    return (len(frames) / a.get_length())


def ball():
    smoothY = 0
    global frameRate
    print('balls frame rate', soundFilePath)
    frameRate = inferFrameRate(frames, soundFilePath)

    print("did inferframerate work? ", frameRate)

    # Load audio
    pygame.mixer.music.load(soundFilePath)

    pygame.mixer.music.play(0, 0.0)

    initTime = time.time()
    pressVal = 0

    # ----------------------------------------------------------------
    #      pygame main loop
    # ----------------------------------------------------------------
    global done
    while not done:

        # This sets the framerate
        # Leave this out and we will use all CPU we can.
        global frameIndex
        #clock.tick_busy_loop(frameRate )
        clock.tick_busy_loop(frameRate - 2)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))

        # interp does what MapRange is supposed to do
        # interp(dataPoint, [from_min,from_max],[to_min,to_max])
        # Rounds and makes frames into integers and translates the range of values in frames into the matching screen dimensions
        # radius and borderGap is added to prevent the ball from being displayed to the edges of the screen and avoid displaying only part of the ball
        framePosition = int(round(interp(frames[frameIndex], [min(frames), max(frames)],
                                         [0 + radius + borderGap, height - radius - borderGap])))

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
                #if event.key == pygame.K_e:
                 #   exportVals(keylogData)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                    pressVal = 0

            #clock.tick(FPS)
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
            gameOver = True
            done = True



def exportVals(klData):

    currentHdfName = sorted_hdf_dirs[trialIndex].split(".")[0]
    currentHdfName = currentHdfName.split('_', 1)[-1]
    print('currentHdfName', currentHdfName)

    # Key Log Data, save in the participant_data folder
    #with open('pid' + pid + '_trial' + str(trial) + '_' + currentHdfName + '.csv', 'w') as csvfile:
    with open('../data/participant_data/' + 'pid' + pid + '_trial' + str(trial) + '_' + currentHdfName + '.csv', 'wb') as csvfile:

        fieldnames = ['time', 'keypress']
        writer = csv.writer(csvfile)
        # writer.writeheader()
        keylogData = klData.items()
        print "writing " +  currentHdfName + ".csv"
        for e in keylogData:
            writer.writerow(e)
        print "finished writing file"


def gameEnd():
    end = True
    global trial

    while end:

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

        pygame.display.update()
        #clock.tick(FPS)
        clock.tick(frameRate)


game_intro()
trialLoop()
gameEnd()

# Be IDLE friendly
pygame.quit()