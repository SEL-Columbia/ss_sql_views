'''
energy_hourly_CSV.py
--------------------

script to create CSV of energy values hourly for all circuits
will output CSV with
rows - individual circuits, identified by pin number
cols - credit sample for each date

warning, dates missing from all circuits to not appear in index
'''

# these lines control whether or not all circuits are queried
filter_by_meter_list = True
meter_list = ['ml01', 'ml02', 'ml03', 'ml04', 'ml07', 'ml08']

# get list of pins corresponding to meters in meter_list
import offline_gateway as og
circuit_dict_list = og.get_circuit_dict_list()

# use subsample while debugging
#circuit_dict_list = circuit_dict_list[:20]

import datetime as dt
date_start = dt.datetime(2012, 1, 1)
date_end   = dt.datetime(2012, 2, 1)

# place time series for credit of each pin in a dictionary
d = {}
for i, c in enumerate(circuit_dict_list):

    if not filter_by_meter_list or c['meter_name'] in meter_list:

        #choose method of labeling data
        #label = c['meter_name'] + '-' + c['ip_address'][-2:]
        label = c['pin']

        # query database
        print 'querying for', i, 'th circuit =', label
        watthours = og.get_watthours_for_circuit_id(c['circuit_id'], date_start, date_end)

        # append to dictionary
        d[label] = watthours

# assemble dictionary into dataframe
import pandas as p
df = p.DataFrame(d)

# transpose dataframe and output to CSV
df.T.to_csv('energy_hourly.csv')
