<b> Useful RRAT Stuff </b>

As the name suggests this repository has, and will have more (!),
tools for dealing with Rotating Radio Transients (RRATs). 

<b> getper </b>

One thing you might want to do is get underlying periodcities when you
have a possibly very high nulling fraction. 

1. CHIME Repeater

CHIME reported a periodicity for one of their repeating FRBs here:
https://arxiv.org/abs/2001.10275. To have a look at that one could
just run the data from their Extended Data Table 1, in the following
way, to get a plot like that in period.png

> python getper.py -i CHIME_seconds -p1 86400.0 -p2 8640000.0 -maxdiff 86400000.0 -pstep 8640.0 -days 1

run with a -h to see what the options are.

2. 12.1-s Pulsar

This code was used to find the period of the 12.1-s pulsar, discovered
in the SUPERB project. See here: https://arxiv.org/abs/1910.04124

A good rule of thumb is that you should have at least 8 'TOAs' (so 28
pairs of TOAs) within a time window where they are all in phase wrt
respect to the uncertainty of the TOA determination
(i.e. sqrt(N)*sigma_TOA << P_trial) and then you will probably find
the right period. More and it is easier. Less and you migt not get it,
or might get a different harmonic. As it happens after the first
detection we thought the 12.1-s pulsar was a 6.05-s pulsar until we
re-observed it and had more pulses to play with.

