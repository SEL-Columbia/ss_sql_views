import sqlalchemy as sa

# create metadata object
metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

# define table objects from database
vpl = sa.Table('view_primary_log', metadata, autoload=True)
m = sa.Table('meter', metadata, autoload=True)

# get meter list from database
query = sa.select([m.c.name], order_by=m.c.name)
result = query.execute()
meter_list = []
for r in result:
    meter_list.append(r.name)

# prune meter list for mali or uganda
meter_list = meter_list[:9]
#meter_list = meter_list[9:]
print meter_list

# query parameters
#meter_name = 'ml03'
date_start = '20111201'
date_end = '20111231'
import datetime as dt
date_start = dt.datetime(2011,12,01)
date_end = dt.datetime(2011,12,31)
ip_mains = '192.168.1.200'

# graph
import pylab
import matplotlib.pyplot as plt
import math
f, ax = plt.subplots(len(meter_list), 1)
f.set_size_inches((16, 16))
for i, meter_name in enumerate(meter_list):
    # sum will show up with key 'sum_1'
    query = sa.select([sa.func.sum(vpl.c.watthours), vpl.c.meter_timestamp],
                      whereclause=sa.and_(vpl.c.meter_name == meter_name,
                                          vpl.c.meter_timestamp > date_start,
                                          vpl.c.meter_timestamp < date_end,
                                          vpl.c.ip_address != ip_mains),
                      group_by=vpl.c.meter_timestamp,
                      order_by=vpl.c.meter_timestamp)
    result = query.execute()

    # parse result into arrays
    dates = []
    watthours = []
    for r in result:
        watthours.append(r.sum_1)
        dates.append(r.meter_timestamp)

    ax[i].plot_date(dates,watthours,label=meter_name)
    ax[i].set_xlim((date_start, date_end))
    ax[i].legend()

#plt.show()
f.savefig('mali_dec.pdf')
