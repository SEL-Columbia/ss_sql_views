Sources of Error
================

Incomplete day of data
----------------------

Occasionally we see the meter begins reporting again in the
middle of the day.  If the first report is near zero, it is
likely that we have missed part of that days consumption.

Methods of identification:

- look for incomplete days of data

Possible algorithm to avoid:

- threshold based on number of reports for that day


SC20 with relay closed but electricity not being metered
--------------------------------------------------------

Methods of identification

- look for change in 'parasitic' consumption of meter


Early ssmeter reset bug
-----------------------

This is a bug in the metering software that causes the watthour value
to be reset at 11pm instead of midnight.  This gives the false reading
of very low power for the day.

Frequency of occurence:

- we will run a query to determine how often this happens.

Possible algorithms to avoid:

- thresholding
- excluding based on watthour drop




SC20 linear watthour drop
-------------------------

Methods of identification:

- sql query to find watthour decreases not occurring at midnight

This is a failure where the reported accumulated watthour value falls
at a rate of a few watthours per hour.

Frequency of occurence:



