

from numpy import interp

import csv
import numpy as np
from scipy.signal import argrelextrema
import math
import os

'''
Analyzing the results:

a,b files already made, just need to be able to read it
a = [time][interp frame]
b = [time][key log]

find local maxes in a, get the time
get the same time and in b to see if it was hit

find where 0 becomes 1 in b = record the index where it is 1
in a list, then get the time

find list of all maxes
get list of all initial key presses

find the difference between the times, then sum it all, compare this sum to other files
only consider the matches that are within a certain range of values.

'''
#TODO Make a folder called MaxMins to store frames in the current directory
#TODO make a folder called Keylogs to store the keylog files in the current directory
#Results will be appended to the current list

global row_count
global timeTracking


# Gnerates list of all files with frames
hdf_dir = 'MaxMins/'
frameString = 'frames'
#hdf_dirs = sorted(os.listdir( hdf_dir ))
sorted_hdf_dirs = sorted(os.listdir( hdf_dir ))
totalfiles = len(sorted_hdf_dirs)
print totalfiles
print "Merged MaxMin"
mergedMaxMin = np.array([])
for file in range(totalfiles):
    mergedMaxMin = np.append(mergedMaxMin, sorted_hdf_dirs[file])
    print sorted_hdf_dirs[file]
print('\n')
print mergedMaxMin[0]
print mergedMaxMin[1]


# Generates list of all files with keylogs
key_dir = 'KeyLogs/'
frameString = 'frames'
#hdf_dirs = sorted(os.listdir( hdf_dir ))
sorted_key_dirs = sorted(os.listdir( key_dir ))
totalfiles = len(sorted_key_dirs)
print totalfiles
print "KeyLogs Dir"
keyLogList = np.array([])

print "KeyLogs"
for file in range(totalfiles):
    print sorted_key_dirs[file]
    keyLogList = np.append(keyLogList, sorted_key_dirs[file])
    print sorted_key_dirs[file]
print('\n')
print "keylog list"
print keyLogList


for file in range(totalfiles):
    frames_file_name = mergedMaxMin[file]

#Merged Max Min
frames_file_name = 'Merged_files_pidv01_trial3_niceBeat_quarter_increase_offset_by_0_frames.csv'
    #keylog_file_name = keyLogList[file]

keylog_file_name = 'pidv01_trial3_niceBeat_quarter_increase_offset_by_0_keylog.csv'


listTimeFrame = np.array([],[])

buf1 = np.ones((10, 2), dtype=np.double)

print "List frame"
print listTimeFrame



with open('MaxMins/' + frames_file_name, 'rb') as f:
    reader = csv.reader(f)
    data = list(reader)
    row_count = len(data)

    buf1 = np.ones((row_count, 2), dtype=np.double)
    print("length of csv: ", row_count)
    print"\n"

    keybuf2 = np.ones((row_count, 2), dtype=np.double)


with open('MaxMins/' + frames_file_name, 'rb') as f:
    index = 0
    reader = csv.reader(f)
    for row in reader:
        #buf1[2] = row
        buf1[index] = row
       # print buf1[index]
        index += 1
        #print ("\n")

    #for n in range(row_count):
    #   buf1[n][1]


# For tracking interp frames
listTimeFrame = buf1
#print listTimeFrame
interp_frames = np.array([])

print buf1[0][1]
for row in range(row_count):
    eachFrameValue = buf1[row][1]
    interp_frames = np.concatenate((interp_frames,[eachFrameValue]))

print "All the frames"
#print interp_frames

# For tracking time
timeTracking = np.array([])

for row in range(row_count):
    eachTimeValue = buf1[row][0]
    timeTracking = np.concatenate((timeTracking,[eachTimeValue]))

#print "All the timelogs"
#print timeTracking


# keylog

interp_frames = np.array([])

print buf1[0][1]
for row in range(row_count):
    eachFrameValue = buf1[row][1]
    interp_frames = np.concatenate((interp_frames,[eachFrameValue]))


with open('KeyLogs/' + keylog_file_name, 'rb') as keyFile:
    keyIndex = 0
    keyReader = csv.reader(keyFile)
    keyLogValueArray = np.array([])
    for row in keyReader:
        #buf1[2] = row
        keybuf2[keyIndex] = row
        #print keybuf2[keyIndex]
        #print keyIndex
        keyIndex += 1
        eachKeyValue = row[1]
        keyLogValueArray = np.concatenate((keyLogValueArray,[int(eachKeyValue)]))


print "Key buff"
print keybuf2

#print "keyLogValueArray"
#print keyLogValueArray


#keylogArray = np.array([0,0,1,1,0,0,1,0])
#print('\n')
#print keylogArray
global firstTapIndexes
firstTapIndexes = np.array([])

print "print keyLogValueArray[0]"
print keyLogValueArray[0]
print keyLogValueArray[112]

for kIndex in range(row_count):
    next = int(kIndex+1)
    #print next
    #print keyLogValueArray[kIndex]
    if next >= row_count:
        break
    if keyLogValueArray[kIndex] == 0 and keyLogValueArray[int(next)] == 1:
        firstTapIndexes = np.concatenate((firstTapIndexes,[int(next)]))

print "firstKeyLogTapIndexes"
print firstTapIndexes


#x = np.random.random(12)
print('\n')
#x =np.array([0.1103653215,0.0724761078,0.0332123538,1, 0.0038404202,7.99883052731948E-05,7.88796385348321E-05])
x = interp_frames

# for local maxima
argrelextrema(x, np.greater)

# for local minima
argrelextrema(x, np.less)


#print x
print ("\n")

print "Local Max Array Positions"
listLocalMaxFramesPos = argrelextrema(x, np.greater)
print listLocalMaxFramesPos
print listLocalMaxFramesPos[0][0]

print ("\n")
print "Local Min Array Positions"
print argrelextrema(x, np.less)

print "Local Max Values"
listLocalMaxFramesVals = x[argrelextrema(x, np.greater)[0]]
print listLocalMaxFramesVals
print ("\n")


#TODO
# Many Local Maxes
print "firstTapIndexes"
print firstTapIndexes
#a = int(firstTapIndexes[1])
#print a
print ("\n")

'''
print timeTracking[a]
print "print listLocalMaxFramesPos"
print listLocalMaxFramesPos[0]
b = listLocalMaxFramesPos[0][1]
print b
print timeTracking[b]

'''

rangeTapsFramesLocalMax = np.array([])

for tap in range(len(firstTapIndexes)):
    tapIndexFilled = False
    for framesIndex in range(len(listLocalMaxFramesPos[0])):
        checkVal = firstTapIndexes[tap]
        upperRange = checkVal + 5
        lowerRange = checkVal - 5
        if listLocalMaxFramesPos[0][framesIndex] > lowerRange and listLocalMaxFramesPos[0][framesIndex] < upperRange and tapIndexFilled == False:
            #if indexFilled == False:
           rangeTapsFramesLocalMax = np.concatenate((rangeTapsFramesLocalMax, [listLocalMaxFramesPos[0][framesIndex]]))
           tapIndexFilled = True
         # don't add duplicates or other numbers within the range, only the first one

print "rangeTapsMax"
print rangeTapsFramesLocalMax



# Does the final calculation of how different the time is with the other one
# really inefficient, but time crunch
calculationList = np.array([])

print "doing calculations"
for tap in range(len(firstTapIndexes)):
    for framesIndex in range(len(rangeTapsFramesLocalMax)):
        checkVal = firstTapIndexes[tap]
        upperRange = checkVal + 5
        lowerRange = checkVal - 5
        if rangeTapsFramesLocalMax[int(framesIndex)] > lowerRange and rangeTapsFramesLocalMax[int(framesIndex)] < upperRange:
            timeDiff = timeTracking[int(firstTapIndexes[tap])]- timeTracking[int(rangeTapsFramesLocalMax[int(framesIndex)])]

            #timeDiffDoubled = timeDiff*2

            #calculationList = np.concatenate((calculationList, [timeDiffDoubled]))
            calculationList = np.concatenate((calculationList, [timeDiff]))

            totalTimeDiff = sum(calculationList)

            print firstTapIndexes[tap]
            print rangeTapsFramesLocalMax[int(framesIndex)]
            print timeDiff

            #print timeDiffDoubled
            print calculationList
            print totalTimeDiff
            print "\n"




#Now save the values into a list to do the calculations
frameTimes = np.array([])
keyLogTimes = np.array([])

print "Local Max Frames with corresponding time"
for n in range(len(rangeTapsFramesLocalMax)):
    frameTimes = np.concatenate((frameTimes, [timeTracking[int(rangeTapsFramesLocalMax[n])]]))
    #print timeTracking[int(rangeTapsMax[n])]
print frameTimes
print "\n"


print "key log taps with corresponding time"
for n in range(len(firstTapIndexes)):
    keyLogTimes = np.concatenate((keyLogTimes, [timeTracking[int(firstTapIndexes[n])]]))
    #print timeTracking[int(firstTapIndexes[n])]
print keyLogTimes
print "\n"

print "!!!!!!!!!!"
print "THE DIFFERENCE IN TIME "
print calculationList
print totalTimeDiff
print "!!!!!!!!!!"
print "\n"


# Calculate the differences between the lists

mismatchCalculation = np.array([])
'''
# really inefficient, but time crunch
for tap in range(len(firstTapIndexes)):
    for framesIndex in range(len(rangeTapsMax)):
        checkVal = firstTapIndexes[tap]
        upperRange = checkVal + 5
        lowerRange = checkVal - 5
        if rangeTapsMax[0][framesIndex] > lowerRange and rangeTapsMax[0][framesIndex] < upperRange:
'''

currentHdfName = keylog_file_name.split(".")[0]
currentHdfName = currentHdfName.split('_', 1)[-1]
currentHdfName = currentHdfName.split(" ")[0]
trialName = currentHdfName.split("_")[0]

print currentHdfName
with open('Calculations/' + 'Total_time_diff_' + '.csv' , 'a') as output:
#with open('Calculations/' + 'Total_time_diff_' + currentHdfName + '.csv', 'w') as output:
    print output
    print('\n')
    writer = csv.writer(output, delimiter=',')
    # writer.writerow(fields) # write a header row
    writer.writerow([trialName, totalTimeDiff])





# Generates list of all files with frames
hdf_dir = 'MaxMins/'
frameString = '_frames.csv'
#hdf_dirs = sorted(os.listdir( hdf_dir ))
sorted_hdf_dirs = sorted(os.listdir( hdf_dir ))

for file in sorted_hdf_dirs:
    if not frameString in file[-11:]:
        sorted_hdf_dirs.remove(file)
#print sorted_hdf_dirs
print('\n')




#TO DO Attempt to plot
from numpy import *

# example data with some peaks:
#data = .2*sin(10*x)+ exp(-abs(2-x)**2)


data = x
# that's the line, you need:
a = diff(sign(diff(data))).nonzero()[0] + 1 # local min+max
b = (diff(sign(diff(data))) > 0).nonzero()[0] + 1 # local min
c = (diff(sign(diff(data))) < 0).nonzero()[0] + 1 # local max

'''
print "b,c"
print b
print c
'''

x= timeTracking

# graphical output...
from pylab import *
plot(x,data, label="Animation")
plot(x[b], data[b], "o", label="min")
plot(x[c], data[c], "o", label="max")
legend()
show()


