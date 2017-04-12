import pygame
from pygame import gfxdraw
from pygame import mixer
from math import pi
from numpy import interp
from numpy import array

import scipy.io.wavfile as wavfile
import numpy as np
import h5py
import pylab

import time
import random
import collections
import csv
import tables

import sys

from tables import *

import glob, os
import os.path

from os import listdir
from os.path import isfile, join

from os import listdir
from os.path import isfile, join

from Tkinter import Tk
from tkFileDialog import askopenfilename


offsetInput = raw_input("Please enter the number of frames you would like to offset by: ")
print "you entered", offsetInput

numOffsetBlanksToAdd = int(offsetInput)

stored_folder = '../data/participant_data/'

# gets current working directory, place where it is ran
current_dir = os.getcwd()
print ("current dir:",current_dir)


Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
selectFilePath = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print("selected file path ", selectFilePath)


selectedFileName = selectFilePath.split("/")[-1].split(".")[0]
print("selected filename ", selectedFileName)
selectedFileNameNoOrder = selectedFileName.split('_', 1)[-1]
print("selected filename without order " ,selectedFileNameNoOrder)

trial = 0
trialIndex = 0
global totalframes
global frames
'''
# TODO works with HDF Dir, use this if we want to create offsets for all the files in the data folders
hdf_dir = '../../data/trials/hdfConditions/'
#hdf_dirs = sorted(os.listdir( hdf_dir ))
sorted_hdf_dirs = sorted(os.listdir( hdf_dir ))

print('sorted hdf_dirs ', sorted_hdf_dirs)

print('0 HDF', sorted_hdf_dirs[0])
print('1 HDF' , sorted_hdf_dirs[1])
print('2 HDF', sorted_hdf_dirs[2])
print('\n')


HDFfilepath = sorted_hdf_dirs[trial]
print('hdffilepath :', sorted_hdf_dirs[trial])


print("Files in HDF")
# This would print all the files and directories
for file in sorted_hdf_dirs:
   print file


# opens h5file
HDFfilepath = os.path.join(hdf_dir, sorted_hdf_dirs[trialIndex])
print('HDF FILE PATH ', HDFfilepath)
#h5file = open_file(HDFfilepath, mode="r+", title="Trial file")
'''


h5file = open_file(selectFilePath, mode="r+", title="Trial file")

# TODO this is where the HDf is chosen (first of the list of sorted HDf files in that folder)
print('h5file ', h5file)
print ('/n')
#table = h5file.animation
table = h5file.root.animation

# constructs array of frame vals
frames = [x for x in table.iterrows()]

# determine the total frames needed in the HDF file
# if we are removing frames, then the total number of frames is the same as the original
# if we are adding frames, add the number of frames to be added to the original number of frames
if numOffsetBlanksToAdd <= 0:
   totalframes = len(frames)
else:
   totalframes  = len(frames) + numOffsetBlanksToAdd

# print("show frames", frames)
print("total num frames", totalframes)
frames = [x for x in table.iterrows()]
# print("show frames", frames)
print("max", max(frames))
print("min", min(frames))


# Create copy of HDF file
# Current displays order of which the HDF file is played, could be removed by uncommenting outselectedFileNameNoOrder
#FILE1 =  selectedFileNameNoOrder + "_offset_by_" + str(numOffsetBlanksToAdd)
FILE1 =  selectedFileName + "_offset_by_" + str(numOffsetBlanksToAdd) + ".hdf"
DATASET1 = "animation"
#FILE2 = "bleeptest.hdf"
#FILE2 = selectedFileNameNoOrder
FILE2 = selectedFileName + ".hdf"
DATASET2 = "animation"


RANK = 2
DIM1 = totalframes
DIM2 = 1
NUMP = 2

#buf1 affects what was in the frame previously
#buf1 = np.zeros((DIM1, DIM2), dtype=np.double)

#this is used to write the original HDF file with the reflected numOffsetBlanktsToAdd
#the rest of the array will be overwirtten by copying the values in frames
buf1 = np.ones((DIM1, DIM2), dtype=np.double)

# Reflect values from the top of the array to the numOffSetBlanksToAdd times
if numOffsetBlanksToAdd >= 0:
   for n in range(numOffsetBlanksToAdd):
      buf1[n] = np.array(frames[numOffsetBlanksToAdd-n])
# Reflect values from the bottom of the array
else:
   # -1 so the last value is not repeated in the tail reflection
   for n in range(abs(numOffsetBlanksToAdd)):
      buf1[totalframes-n-1]= np.array(frames[totalframes-abs(numOffsetBlanksToAdd)+n-1])
   # numOffsetBlanksToAdd reverses the list from the set n


print("buf1, ", buf1)
fid1 = h5py.h5f.create(FILE1)
dims = (DIM1, DIM2)
space1 = h5py.h5s.create_simple(dims)

dset1 = h5py.h5d.create(fid1, DATASET1, h5py.h5t.NATIVE_DOUBLE, space1)

dset1.write(h5py.h5s.ALL, h5py.h5s.ALL, buf1)


# Open the two files.  Select two point in one file, write values to
    # those point locations, then copy and write the values to the other
    # file.

file1 = h5py.h5f.open(FILE1)
dset1 = h5py.h5d.open(file1, DATASET1)

file2 = h5py.h5f.open(FILE2)
dset2 = h5py.h5d.open(file2, DATASET2)

fid1 = dset1.get_space()
mid1 = h5py.h5s.create_simple((len(frames),))
#mid1 = h5py.h5s.create_simple((totalframes,))

# Open the two files.  Select two point in one file, write values to
# those point locations, then copy and write the values to the other
# file.
#coord = np.zeros((NUMP, RANK))

#coord = np.ones((totalframes,2))
coord = np.ones((len(frames),2))
print "coord!!" ,coord
#coord = np.zeros((len(frames),2))
#copyCoord = np.zeros((numOffsetBlanksToAdd,2))
#numOffsetAddCoord = np.ones((numOffsetBlanksToAdd,2))
#print ("copycoord ", copyCoord)

# The max times the for loop has to check each frame value in the original HDF file
maxRange = len(frames)

print("FRAME 0:", frames[0])
print("FRAME 1:", frames[1])
# checks if the input value is positive or negative
# if the x coordinate becomes a negative value then do not add it (remove these frames)
# only add x coordinates that are positive

# If the input value is positive, copy entire frames list but shifted down by the number of input numOffsetBlanksToAdd
if numOffsetBlanksToAdd >= 0:
   for i in range(maxRange):
      if numOffsetBlanksToAdd > 0:
         coord[i] = [i+numOffsetBlanksToAdd,0]
# Case wehere the input numOffsetBlanksToAdd is a negative value, copy the frames list removing the top numOffsetBlanksToAdd from the top
else:
   for i in range(maxRange):
      if i + numOffsetBlanksToAdd + 1 > 0:
         coord[i] = [i + numOffsetBlanksToAdd, 0]

'''


for n in range(numOffsetBlanksToAdd):
   numOffsetAddCoord[n] = [n + numOffsetBlanksToAdd,0]


for n in range(numOffsetBlanksToAdd):
   copyCoord[n] = [n + numOffsetBlanksToAdd,0]
print ("copycoordAFTER ", copyCoord)

for i in range(totalframes):
   if numOffsetBlanksToAdd > 0:
      if i+numOffsetBlanksToAdd < totalframes:
         coord[i] = [i + numOffsetBlanksToAdd, 0]
for n in range(numOffsetBlanksToAdd):
         # coord[n]= [frames[n],0]
   coord[n] = copyCoord[n]
   print("coord",coord[n])

for n in range(numOffsetBlanksToAdd):
            # coord[n]= [frames[n],0]
   coord[n] = numOffsetAddCoord[n]
'''
         #coord[n] = [numOffsetBlanksToAdd-n-1, 0]

         #coord[i+n] = [i+numOffsetBlanksToAdd,0]
   #else:
      #if i + numOffsetBlanksToAdd > 0:
      #   coord[i] = [i + numOffsetBlanksToAdd, 0]

#order in the coppied file = [coordinates of where to place it in the hdf file)
'''coord[0] = [2,0]
coord[1]=[1,0]
coord[2]=[0,0]
copyCoord[0]=[0,0]
'''
#coord[len(frames)] = [0,0]
#coord[0]= [1,0]
#coord[1]=[3,0]
#coord[2] =[2,0]

'''
coord[0] = [0, 0]
coord[1] = [1, 0]
coord[2] = [2, 0]
coord[3] = [3, 0]
print("coord[0]",coord[0] )
print("coord[1]",coord[1])
print("coord[2]",coord[2])
print("coord[3]",coord[3])
'''
# prints the coordinates in the HDF File
print('coord ', coord)
fid1.select_elements(coord)
print("fid1", fid1.select_elements(coord))
print("fid1",fid1)

# The values to be copied
val = np.array(frames, dtype=np.double)
#val = np.array(frames)
#var = 12
#val = np.append(var, val[0])
print('/n')
#print('values to be copied ', val)



# Write selected file's contents into empty hdf file (copy)
dset1.write(mid1, fid1, val, h5py.h5t.NATIVE_DOUBLE)


# Open both files and print the contents of the datasets.
file1 = h5py.h5f.open(FILE1)
# file2 = h5py.h5f.open(sorted_hdf_dirs[trialIndex])
file2 = h5py.h5f.open(FILE2)
dset1 = h5py.h5d.open(file1, DATASET1)
dset2 = h5py.h5d.open(file2, "animation")

bufnew = np.ones((DIM1, DIM2), dtype=np.double)
dset1.read(h5py.h5s.ALL, h5py.h5s.ALL, bufnew)

'''
#Debugging, quick view of what is in the copied HDF file
print("\nDataset '%s' in file '%s' contains:" % (DATASET1, FILE1))
print(bufnew)
'''



