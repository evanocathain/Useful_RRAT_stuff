#!/usr/bin/python

from sympy import *
import numpy as np
import scipy as sp
from scipy.stats import skew
import matplotlib.pylab as plt
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-p1', type=float, dest='p1', help='set the lowest period (default: 0.1 seconds)', default=0.100)
parser.add_argument('-p2', type=float, dest='p2', help='set the lowest period (default: 10.0 seconds)', default=10.0)
parser.add_argument('-i', dest='input_file', help='set the input file name (default: file)', default="file")
parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
args = parser.parse_args()

# Read in times
input_file = args.input_file
print "Reading input from file:",input_file
times = np.genfromtxt(input_file)
#for i in range(0,np.size(times)):
#    print times[i]
times.sort()
#for i in range(0,np.size(times)):
#    print times[i]
ntimes = np.size(times)
print "Total number of pulse times:",ntimes

# Get the time differences
max_diff = 1000.0
pstep = 0.001
diffs = np.zeros(ntimes*ntimes)
k = 0
for i in range(0,ntimes):
    for j in range(0,ntimes):
        diff = times[j] - times[i]
        if ( diff <= max_diff):
            if ( diff < 0.0 ):
                diffs[k] = - diff
            else:
                diffs[k] = diff
            k = k+1
#            print "%.3f"%diff

diffs.sort()
diffs_unique = np.unique(diffs)
print "Total number of unique time differences:",np.size(diffs_unique)

# Search period range
p1 = args.p1
p2 = args.p2
pstep = 0.001
nsteps = int((p2 - p1)/pstep)
print "Searching from",p1,"to",p2,"in",nsteps,"steps"

periods = np.zeros(nsteps)
matches = np.zeros(nsteps)
for i in range(0,nsteps):
    periods[i] = p1+i*pstep
    for j in range(0,np.size(diffs_unique)):
        phase = (diffs_unique[j]/periods[i]) - int(diffs_unique[j]/periods[i])
#        print diffs_unique[j], periods[i], phase
        if ( phase < 0.10 ):
            matches[i] = matches[i] + 1
plt.ylabel("Number of matches")
plt.xlabel("Trial Period (s)")
plt.plot(periods,matches)
plt.show()
