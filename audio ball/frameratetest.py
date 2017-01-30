import pygame
import sys
import time
from OpenGL.GL import *
from OpenGL.GLU import *
#Timing code at the END!
    curr_time = time.time()#so now we have time after processing
    diff = curr_time - prev_time#frame took this much time to process and render
    delay = max(1.0/target_fps - diff, 0)#if we finished early, wait the remaining time to desired fps, else wait 0 ms!
    time.sleep(delay)
    fps = 1.0/(delay + diff)#fps is based on total time ("processing" diff time + "wasted" delay time)
    prev_time = curr_time
    pygame.display.set_caption("{0}: {1:.2f}".format(title, fps))
title = "FPS Timer Demo"
target_fps = 60
(width, height) = (300, 200)
flags = pygame.DOUBLEBUF|pygame.OPENGL
screen = pygame.display.set_mode((width, height), flags)

rotation = 0
square_size = 50
prev_time = time.time()

while True:
    #Handle the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #Do computations and render stuff on screen
    rotation += 1
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslate(width/2.0, height/2.0, 0)
    glRotate(rotation, 0, 0, 1)
    glTranslate(-square_size/2.0, -square_size/2.0, 0)
    glBegin(GL_QUADS)
    glVertex(0, 0, 0)
    glVertex(50, 0, 0)
    glVertex(50, 50, 0)
    glVertex(0, 50, 0)
    glEnd()
    pygame.display.flip()

    #Timing code at the END!
    curr_time = time.time()#so now we have time after processing
    diff = curr_time - prev_time#frame took this much time to process and render
    delay = max(1.0/target_fps - diff, 0)#if we finished early, wait the remaining time to desired fps, else wait 0 ms!
    time.sleep(delay)
    fps = 1.0/(delay + diff)#fps is based on total time ("processing" diff time + "wasted" delay time)
    prev_time = curr_time
    pygame.display.set_caption("{0}: {1:.2f}".format(title, fps))