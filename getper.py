#!/usr/bin/env python

import argparse
import os.path
import sys

import matplotlib.pylab as plt
import numpy as np


def parse_args():
    """
    Parse the commandline arguments.

    Returns
    -------
    args: populated namespace
        The commandline arguments.
    """

    parser = argparse.ArgumentParser(
        description='Determine period by arrival time differencing.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'filename',
        help='input file name'
    )

    parser.add_argument(
        '-p1',
        type=float,
        dest='p1',
        help='set the lowest trial period in seconds',
        default=0.100
    )

    parser.add_argument(
        '-p2',
        type=float,
        dest='p2',
        help='set the highest trial period in seconds',
        default=10.0
    )

    parser.add_argument(
        '-days',
        dest='days',
        action='store_true',
        help='plot output in days rather than seconds',
        default=False
    )

    parser.add_argument(
        '-maxdiff',
        type=float,
        dest='maxdiff',
        help='maximum time difference in seconds to use',
        default=3600.0
    )

    parser.add_argument(
        '-mjd',
        dest='mjd',
        action='store_true',
        help='flag input times as MJD rather than seconds',
        default=False
    )

    parser.add_argument(
        '-pstep',
        type=float,
        dest='pstep',
        help='trial period step size in seconds',
        default=0.001
    )

    parser.add_argument(
        '-tol',
        type=float,
        dest='tol',
        help='percentage tolerance in phase to count as a match',
        default=10.0
    )

    parser.add_argument(
        '--version',
        action='version',
        version='0.0.3'
    )

    args = parser.parse_args()

    return args


def plot_matches(periods, matches, args):
    """
    Plot the matches versus trial period.

    Parameters
    ----------
    periods: ~np.array
        The trial periods.
    matches: ~np.array
        The number of matches corresponding to the trial periods.
    args: populated namespace
        The commandline arguments.
    """

    fig = plt.figure()
    ax = fig.add_subplot(111)

    if args.days:
        ax.plot(periods / 86400.0, matches)
        ax.set_xlabel("Trial Period (days)")
    else:
        ax.plot(periods, matches)
        ax.set_xlabel("Trial Period (s)")

    ax.grid()
    ax.set_ylabel("Number of matches")


#
# MAIN
#

def main():
    args = parse_args()

    ## Read in data
    # Read in barycentred times
    if not os.path.isfile(args.filename):
        print('The file does not exist: {0}'.format(args.filename))
        sys.exit(1)

    print("Reading input from file: {}".format(args.filename))
    times = np.genfromtxt(args.filename)
    times = np.sort(times)
    ntimes = np.size(times)
    print("Total number of pulse times: {0}".format(ntimes))
    print("Total number of unique time differences: {0}".format(ntimes * (ntimes - 1) / 2.0))

    # If input times in MJD, convert to seconds
    if args.mjd:
        times = (times - int(np.floor(times[0]))) * 86400.0

    ## Get the time differences
    maxdiff = args.maxdiff
    diffs = np.zeros(ntimes * ntimes)
    k = 0
    for i in range(0, ntimes):
        for j in range(0, ntimes):
            diff = times[j] - times[i]
            if np.abs(diff) <= maxdiff:
                if diff < 0.0:
                    diffs[k] = - diff
                else:
                    diffs[k] = diff
                k = k+1

    diffs = np.sort(diffs)
    diffs_unique = np.unique(diffs)
    print("Total number of unique time differences less than {0} seconds: {1}".format(
        maxdiff,
        np.size(diffs_unique)
        )
    )
    print(diffs_unique)

    ## Search period range
    p1 = args.p1
    p2 = args.p2
    pstep = args.pstep
    nsteps = int((p2 - p1) / pstep)
    print("Searching from {0} to {1} in {2} steps".format(
        p1,
        p2,
        nsteps
        )
    )

    # Number of matches within X percent
    phase_tol = args.tol * 0.01
    periods = np.zeros(nsteps)
    matches = np.zeros(nsteps)

    for i in range(0, nsteps):
        periods[i] = p1 + i * pstep
        for j in range(0, np.size(diffs_unique)):
            phase = (diffs_unique[j] / periods[i]) - int(diffs_unique[j] / periods[i])
            if ( (phase < 0.5 * phase_tol) or (phase > (1.0 - 0.5 * phase_tol))):
                matches[i] = matches[i] + 1

    plot_matches(periods, matches, args)

    plt.show()


if __name__ == '__main__':
    main()
