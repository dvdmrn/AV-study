# File names and functionality descriptions:

## AV-study/stim_delivery/ (Folder) 

### AV-study/stim_delivery/Results_Analysis (Folder) 
- FindMaxMinSingle.py
  -	Analyse the results from the the interp frame, key logs and time
  -	Find all the local maxes in the interp frame and time excel file 
  -	Find all the indexes where spacebar is pressed on (key log is first pressed) 
-	FindMaxMinsManyAutomate.py
  -	Same features as FindMaxMinSingle.py, except this runs the script for all the files in the folder and finds the files which contain the string ‘frames’ and the corresponding trial files with keylogging 
  -	Make sure to comment out the plot and graph section of the code or else the program will continuously generate and display graphical pop-ups. 
- Cross_correlation.py
  -	pearson and numpy correlation coefficient calculations 
-	Tompy.py
  -	Necessary imports and column checks for coefficient calculations by Tom Irvine 

### AV-study/stim_delivery/animationplayer (Folder) 
-	CreateHdfOnsets/ (Folder)  
	- hdfOnsetReflectedNoBlanks.py
		- number of frames. The number of frames 
  - hdfOnset.py
    - Simpler features of hdfOnsetReflectedNoBlanks.py, except instead of reflecting the number of frames, blanks (zeros) are added by the input number of positive integers or frames are removed if the input number is a negative integer 
    - Other HDF files are the generated output files from either of the two .py scripts, one HDF file must be the file generated from the animationplayer which is used in the script to generate the other HDF files (adds the input integer into the created file name to the  name of the original HDF file) (original:  0_niceBeat.hdf, created HDF file with input integer of 10 0_niceBeat_offset_by_10.hdf). 
-	stimDeliveryWithKeylog.py
    -	Records time and frames during trials and generates an excel sheet 
    -	Frames from the HDF files are scaled to a range between 0 to 1 for more efficient and easier use with results analysis and for generating more comparable graphs and data with key logging. This is because keylogging is recorded with 0 to 1, so graphs or other data analysis methods to compare the frames with the same range from 0 to 1, would make analyzing the results more convenient. 

- stimDeliveryWithKeylogTwoFiles.py
    -	Same functionality as above, except the frames is measured differently. 
    -	Frames are recorded as the same value as the frame inputs in the given HDF files. If this .py file was used, it can be converted to the scaled values in the above file, but requires more work by using more scripts and reorganizing data in folders. 
-	stimDelivery.py
     -	Backup of earlier renditions of stimDelivery with the added screens and trial messages during the experiment. 
-	Keylog_data.py
    -	Script for generating a csv (keylog_data.csv) which records the time and the frequency of the user pressing the spacebar and holding the spacebar during the experiment. (pressing the spacebar indicates the user detected the ball bounced up to the peak)
-	AV-study/stim_delivery/data/trials (Folder)  
	-	hdfConditions (Folder) 
   	 	- Place HDF files in this folder to be used for the trials in the experiment
   		-	Played in the order they are numerically arranged 
	-	wavConditions (Folder) 
   	 	-	Place wav files in this folder to be used for the trials in the experiment
   	 	-	Played in the order they are numerically arranged, the same wav files can be played multiple times when setting up the experiment for the participant  

## stimDeliveryWithKeyLog.py
- **Functionality:** Runs the experiment with the different trials, displays the interface for the different screens and the trials
- **Input:** takes in the HDF files and the WAV files found in the "AV-study/stim_delivery/data/participant_data” folder. Iterates throughout the entire list
- **Output:** two CSV files, one CSV file with the time and keylog data, another file with time and frames displayed per trial. The frame rate can either be converted to be from a scale from 0 to 1, or from the input HDF file which was use to create the trial

## FindPeaks.py  
- **Functionality:** does the calculations to find where the crests are from the participant recorded data.
- looks at the frames from the HDF excel files and finds the local maximas 
- finds all the locations where the key logs are initially pressed (when the keylog was 0 initially which means the space bar was not pressed, until the the spacebar is pressed. (records the indexes of where the the key ogs are from 0 to 1)

## cross_correlation.py
- **Functionality:** calculates the cross-correlation and allows user to select to separate files to analyze what their cross correlation is and multiple statistical results as well as display a chart of the two input files and a third file of the cross-correlation.
- **Input:** select the two files used to calculate the cross-correlation between 
- **Output:** on console the statistical calculations and graphs.



## hdfOnsetAddBlanks.py
- **Functionality:** adds the user input n number of blanks in front of the given HDF file 
- **Input:** HDF file path and the number of frames you would like to offset the HDF file by. Can input a negative number to remove frames and a positive number to add blank frames before the given HDF file 
- **Output:** new hdf file with the user input number of blank frames before the original HDF file  (positive input value) or the user input number of frames removed from the original HDF file (negative input value) 

## hdfOnsetReflectedNoBlanks.py
- **Functionality:** creates HDF files with user input amount of frames to offset the input file by.
- **Input:** HDF file created from the animation player or a regular HDF file. 
- **Output:** new HDF file with the user indicated amount of offset. Based on the n input from the user, the tail or the head of the file will be reflected by the same number of n frames 
