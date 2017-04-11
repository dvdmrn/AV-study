##########################################################################
# program: cross_correlation.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.3
# date: September 12, 2013
#
"""
  Calculate the cross_correlation of two time histories.
  Each file must have two columns: time(sec) & amplitude.
  The files must have the same sample rate.
"""
##########################################################################

from __future__ import print_function

from tompy import read_two_columns,signal_stats,sample_rate_check
from tompy import time_history_plot

from numpy import array,linspace,argmax

from scipy.signal import correlate

import matplotlib.pyplot as plt



from scipy.stats.stats import pearsonr
import numpy as np

    
########################################################################        


print ("Each file must have two columns: time(sec) & accel(G)")

a1,b1,num1 =read_two_columns()

sr1,dt1,mean1,sd1,rms1,skew1,kurtosis1,dur1=signal_stats(a1,b1,num1)

sr1,dt1=sample_rate_check(a1,b1,num1,sr1,dt1)

########################################################################

a2,b2,num2 =read_two_columns()

sr2,dt2,mean2,sd2,rms2,skew2,kurtosis2,dur2=signal_stats(a2,b2,num2)

sr2,dt2=sample_rate_check(a2,b2,num2,sr2,dt2)

########################################################################

a1=array(a1)
b1=array(b1)

#print ("a1 time: ", a1)
#print ('/n')


#print ("b1 keylogs: ", b1)
#print ('/n')

a2=array(a2)
b2=array(b2)       

#print ("a2 time: ", a2)
#print ('/n')

#print ("b2 frames: ", b2)
#print ('/n')

if((dt1-dt2)/dt2 < 0.001):

    if(num1<num2):
        a2=a2[0:num1]        
        b2=b2[0:num1]    

    if(num1>num2):
        a1=a1[0:num2]        
        b1=b1[0:num2]


    #TODO Coefficient Calculation

    # Calculates a Pearson correlation coefficient and the p-value for testingnon-correlation.
    # Only calculates  The Pearson correlation coefficient measures the linear relationshipbetween two datasets.
    # Strictly speaking, Pearson's correlation requiresthat each dataset be normally distributed.
    #  Like other correlationcoefficients, this one varies between -1 and +1 with 0 implying nocorrelation.

    print("Pearson Linear Correlation and P-value")
    #print(pearsonr([1, 2, 3], [5, 8, 10]))
    print(pearsonr(b1, b2))
    print('\n')

    #numpys version of coefficient
    list1 = [1, 2, 3]
    list2 = [3, 5, 7]

    print("Numpy Correlate Coefficient: ")
    #np.corrcoef(list1, list2)[0, 1]
    print(np.corrcoef(b1, b2)[0, 1])


    # information for plots

    cc = correlate(b1,b2)

    n=len(cc)

    cc=2*cc/n

    dur=n*dt1/2;
    d=linspace( -dur, dur, n )


    idx = argmax(cc) 
    
    print (" ")
    print (" Maximum:  Delay=%8.4g sec   Amp=%8.4g " %(d[idx],cc[idx]))

    title_string= "Cross-correlation  Max: Delay=%6.3g sec   Amp=%7.4g " %(d[idx],cc[idx])

    print (" ")
    print (" view plots")

    time_history_plot(a1,b1,1,'Time(sec)','Amplitude','Input Time History 1','time_history_1')

    time_history_plot(a2,b2,2,'Time(sec)','Amplitude','Input Time History 2','time_history_2')
    
    time_history_plot(d,cc,3,'Delay(sec)','Rxy',title_string,'cross_correlation')

    plt.show()




else:
    
    print (" ")
    print (" dt error ")