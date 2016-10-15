import pygame
from pygame import gfxdraw
from math import pi

import scipy.io.wavfile as wavfile
import numpy
import pylab

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
 
# Set the width and height of the screen
size = [width,height]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Audio Ball")
 
#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
 

#plots wav of left channel
rate,data = wavfile.read('sampletone.wav')

#Draw a circle
    #   unfortunately if you want antialiasing support is only available for
    #   the outline of a circle, so we must draw the filled circle beneath the outlined
    #   circle.
def circle(x,y,r,color):
        pygame.gfxdraw.filled_circle(screen,x,y,r,color)
        pygame.gfxdraw.aacircle(screen,x,y,r,color)

while not done:
 
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(30)

    xPos += 1
    yPos += 3
     
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
     
    # Clear the screen and set the screen background
    screen.fill(WHITE)
 
    circle((width/2),yPos,40,RED)
 

    # Updates screen: this MUST happen after all the other drawing commands.
    pygame.display.flip()
 
# Be IDLE friendly
pygame.quit()