'''
script to create CSV of credit values for all circuits
will output CSV with
rows - individual circuits, identified by pin number
cols - credit sample for each date

warning, dates missing from all circuits to not appear in index
'''

meter_list = ('ml01','ml02','ml03','ml04','ml07','ml08')

# get list of pins corresponding to meters in meter_list
import offline_gateway as og
pins = og.get_pins(meter_list)

import datetime as dt
date_start = dt.datetime(2011,9,1)
date_end = dt.datetime(2012,2,1)

# place time series for credit of each pin in a dictionary
d = {}
for i, pin in enumerate(pins):
    print 'querying for', i, 'th pin =', pin
    credit = og.get_credit_for_pin(pin, date_start, date_end)
    d[pin] = credit

# assemble dictionary into dataframe
import pandas as p
df = p.DataFrame(d)

# transpose dataframe and output to CSV
df.T.to_csv('credit.csv')
