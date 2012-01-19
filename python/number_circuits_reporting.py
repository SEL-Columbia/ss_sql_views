'''
simple script to plot total number of meters reporting as a time series.
There is no averaging and the resolution is hourly.
If there are zero meters reporting, the sample is omitted.
'''

# query over view_primary_log grouping by timestamp

# print out timeseries to matplotlib

import datetime as dt
date_start = dt.datetime(2011, 12, 01)
date_end = dt.datetime(2012, 01, 31)

import sqlalchemy as sa

# create metadata object
metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

# define table objects from database
vpl = sa.Table('view_primary_log', metadata, autoload=True)


query = sa.select([vpl.c.meter_timestamp,
                   sa.func.count(vpl.c.watthours).label('num_meters')],
                   whereclause=sa.and_(vpl.c.meter_timestamp > date_start,
                                       vpl.c.meter_timestamp < date_end),
                   group_by=vpl.c.meter_timestamp,
                   order_by=vpl.c.meter_timestamp)

result = query.execute()

timestamp = []
num_meters = []
for r in result:
    timestamp.append(r.meter_timestamp)
    num_meters.append(r.num_meters)

import matplotlib.pyplot as plt
f, ax = plt.subplots(1, 1)

ax.plot_date(timestamp, num_meters, 'ko-')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Circuits Reporting')
f.autofmt_xdate()

f.savefig('number_circuits_reporting.pdf')