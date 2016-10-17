#----------------------------------------------------------------
# Run this script by typing:
#	python ballHDF.py <HDF_file_path> <sound_file_path>
# Note: sounds must be a wav file!
#----------------------------------------------------------------


import pygame
from pygame import gfxdraw
from pygame import mixer
from math import pi

import scipy.io.wavfile as wavfile
import numpy
import pylab

from tables import *

import sys

HDFfilepath = sys.argv[1]
soundFilePath = sys.argv[2]

#----------------------------------------------------------------
#      pytables
#----------------------------------------------------------------

class Animation(IsDescription):
    frame = Float64Col()

#opens h5file
h5file = open_file(HDFfilepath, mode = "r", title = "Test file")
table = h5file.root.animation
#constructs array of frame vals
frames = [x for x in table.iterrows()]

#will be used to interate frames in main loop
frameIndex = 0


#----------------------------------------------------------------
#      pygame setup
#----------------------------------------------------------------


# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

#circle position
xPos = 0
yPos = 0
#window params
height = 480
width = 640

ballColor = BLUE
# Set the width and height of the screen
size = [width,height]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Audio Ball")
 
#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

scaleFactor = 100


#Load audio
pygame.mixer.music.load(soundFilePath)

pygame.mixer.music.play(-1, 0.0)
#Draw a circle
    #   unfortunately if you want antialiasing support is only available for
    #   the outline of a circle, so we must draw the filled circle beneath the outlined
    #   circle. :( 
def circle(x,y,r,color):
        pygame.gfxdraw.filled_circle(screen,x,y,r,color)
        pygame.gfxdraw.aacircle(screen,x,y,r,color)

def inferFrameRate(frames,soundFilePath):
	a = pygame.mixer.Sound(soundFilePath)
	print("length of sound file: ",a.get_length())
	print("number of frames: ", len(frames))
	return (len(frames)/a.get_length())
	

framerate = inferFrameRate(frames,soundFilePath)

print("did inferframerate work? ", framerate)

#----------------------------------------------------------------
#      pygame main loop
#----------------------------------------------------------------

while not done:
 
    # This sets the framerate
    # Leave this out and we will use all CPU we can.
    clock.tick(framerate)
    

    framePosition = int(round(frames[frameIndex]*scaleFactor))
    xPos += 1
    yPos = (height/2) - framePosition
    if yPos < 0:
    	yPos = 0
    if yPos > height:
    	yPos = height
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
     
    # Clear the screen and set the screen background
    screen.fill(WHITE)
 
    circle((width/2),yPos,40,ballColor)
 
    frameIndex+=1
    # Updates screen: this MUST happen after all the other drawing commands.
    pygame.display.flip()
 
# Be IDLE friendly
pygame.quit()