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

from tables import *

import sys

HDFfilepath = sys.argv[1]
soundFilePath = sys.argv[2]


# ----------------------------------------------------------------
#      pytables
# ----------------------------------------------------------------

class Animation(IsDescription):
    frame = Float64Col()


# opens h5file
h5file = open_file(HDFfilepath, mode="r", title="Test file")
table = h5file.root.animation
# constructs array of frame vals
# !!! min max values can be found in here \/ below
frames = [x for x in table.iterrows()]
# print("show frames", frames)
print("max", max(frames))
print("min", min(frames))

# will be used to interate frames in main loop
frameIndex = 0

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
width = 640
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

pygame.display.set_caption("Audio Ball")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

# TODO:
#  1. Get min/max pos. values of the screen                     0, height, 0, width
#  2. Get min/max pos. values of the HDF animation file         max(frames), min(frames)
#  3. Write/implement mapRange() function (look up on SO or something)   interp(data,[from_min,from_max],[to_min,to_max])
#  4. Map everything in frames to the screen's min/max vals
#  5. remove scaleFactor
#  voice file, haber, test with diff hdf files
# scaleFactor = 100


# Load audio
pygame.mixer.music.load(soundFilePath)

pygame.mixer.music.play(-1, 0.0)


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


framerate = inferFrameRate(frames, soundFilePath)

print("did inferframerate work? ", framerate)

# ----------------------------------------------------------------
#      pygame main loop
# ----------------------------------------------------------------

while not done:

    # This sets the framerate
    # Leave this out and we will use all CPU we can.

    clock.tick_busy_loop(framerate - 2)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

    # get position from a cell in the HDF file
    # framePosition = int(round(frames[frameIndex]*scaleFactor))

    # interp does what MapRange is supposed to do
    # interp(dataPoint, [from_min,from_max],[to_min,to_max])
    # Rounds and makes frames into integers and translates the range of values in frames into the matching screen dimensions
    # radius and borderGap is added to prevent the ball from being displayed to the edges of the screen and avoid displaying only part of the ball
    framePosition = int(round(
        interp(frames[frameIndex], [min(frames), max(frames)], [0 + radius + borderGap, height - radius - borderGap])))

    # framePosition = int(round(interp(frames[frameIndex], [min(frames), max(frames)], [0,height])))

    # keep track of frame changes
    # print("framePos:" , framePosition)



    # xPos += 1
    # set y pos.
    # yPos = (height/2) - framePosition
    # Converted this to Positive values similar to how the screen is displayed.
    # Made more inuitive sense to me
    yPos = abs(framePosition - height)

    # print("frameposition", framePosition)

    if yPos < 0:
        yPos = 0
    # boundary checking
    if yPos > height:
        yPos = height

    # Keep track of yPos
    # print("yPos:", yPos)
    # Testing
    '''
    #print("frameposition", framePosition)
    if yPos <= 0:
    	yPos = (0 + radius + borderGap)
    #     boundary checking
    if yPos >= height:
    	yPos = (height-radius - borderGap)
    '''

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # Clear the screen and set the screen background
    screen.fill(WHITE)

    circle((width / 2), yPos, radius, ballColor)

    frameIndex += 1
    # Updates screen: this MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()