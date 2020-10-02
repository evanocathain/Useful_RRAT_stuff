#!/usr/bin/python

# Load some packages
import numpy as np
import scipy as sp
#from scipy.stats import skew
import matplotlib.pylab as plt
import argparse
import sys

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='input_file', help='set the input file name (default: file)', default="file")
parser.add_argument('-p1', type=float, dest='p1', help='set the lowest period (default: 0.1 seconds)', default=0.100)
parser.add_argument('-p2', type=float, dest='p2', help='set the lowest period (default: 10.0 seconds)', default=10.0)
parser.add_argument('-days', dest='days', help='plot output in days rather than seconds (default: seconds)', default=False)
parser.add_argument('-maxdiff', type=float, dest='maxdiff', help='maximum time difference to use (default: 3600.0 seconds)', default=3600.0)
parser.add_argument('-mjd', dest='mjd', help='flag input times as MJD rather than seconds (default: false)', default=False, action = 'store_true')
parser.add_argument('-pstep', type=float, dest='pstep', help='trial period step size in seconds (default: 0.001)', default=0.001)
parser.add_argument('-tol', type=float, dest='tol', help='percentage tolerance in phase to count as a match (default: 10.0)', default=10.0)
parser.add_argument('--version', action='version', version='%(prog)s 0.0.3')
args = parser.parse_args()

## Read in data
# Read in barycentred times
input_file = args.input_file
print("Reading input from file:",input_file)
times = np.genfromtxt(input_file)
times.sort()
ntimes = np.size(times)
print("Total number of pulse times:",ntimes)
print("Total number of unique time differences:",ntimes*(ntimes-1)/2)
# If input times in MJD, convert to seconds
mjd = args.mjd
if mjd:
    times = (times-int(times[0]))*86400.0

## Get the time differences
maxdiff = args.maxdiff
#pstep = args.pstep*0.001
pstep = args.pstep

samples0 = np.array(times).reshape(-1, 1)
samples1 = np.array(times).reshape(1, -1)

delta = np.triu(np.abs(samples0 - samples1))
delta = delta[delta < maxdiff]
diffs_unique = np.unique(delta).reshape(1,-1)

print("Total number of unique time differences less than ",maxdiff," seconds:",np.size(diffs_unique))
print(diffs_unique)

## Search period range
p1 = args.p1
p2 = args.p2
#pstep = 0.001
nsteps = int((p2 - p1)/pstep)
print("Searching from",p1,"to",p2,"in",nsteps,"steps")

# Number of matches within 10 percent
phase_tol = args.tol*0.01
periods = np.zeros(nsteps)

periods = (p1 + np.arange(nsteps) * pstep).reshape(-1, 1)
phase = (diffs_unique/periods) - (diffs_unique/periods).astype(int)

locs = np.less(phase, 0.5 * phase_tol)
locs += np.greater(phase, 1.0-0.5*phase_tol)

matches = np.sum(locs, axis = 1)

## Plot the matches
plt.ylabel("Number of matches")
days=args.days
if args.days:
    plt.xlabel("Trial Period (days)")
    plt.plot(periods/86400.0,matches)
else:
    plt.xlabel("Trial Period (s)")
    plt.plot(periods,matches)
plt.show()
