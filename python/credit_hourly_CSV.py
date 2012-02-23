'''
credit_hourly_CSV.py
--------------------

script to create CSV of credit values hourly for all circuits
will output CSV with
rows - individual circuits, identified by pin number
cols - credit sample for each date

warning, dates missing from all circuits to not appear in index
'''

# these lines control whether or not all circuits are queried
filter_by_meter_list = True
meter_list = ['ml01', 'ml02', 'ml03', 'ml04', 'ml07', 'ml08']

# use subsample while debugging
#circuit_dict_list = circuit_dict_list[:20]

# choose method of labeling data
method = 'meter'
#method = 'pin'

# choose date range
import datetime as dt
date_start = dt.datetime(2012, 1, 1)
date_end   = dt.datetime(2012, 2, 1)

# get list of pins corresponding to meters in meter_list
import offline_gateway as og
circuit_dict_list = og.get_circuit_dict_list()

# place time series for credit of each pin in a dictionary
d = {}
for i, c in enumerate(circuit_dict_list):

    if not filter_by_meter_list or c['meter_name'] in meter_list:

        # generate appropriate dictionary key
        if method == 'meter':
            label = c['meter_name'] + '-' + c['ip_address'][-2:]
        if method == 'pin':
            label = c['pin']

        # query database and append to dictionary
        print 'querying for', i, 'th circuit =', label
        d[label] = og.get_credit_for_circuit_id(c['circuit_id'], date_start, date_end)

# assemble dictionary into dataframe
import pandas as p
df = p.DataFrame(d)

# transpose dataframe and output to CSV
filename = 'credit_hourly_' + str(date_start.year) + '-' + str(date_start.month)
filename += '_' + method + '.csv'
df.T.to_csv(filename)
