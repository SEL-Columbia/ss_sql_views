import sqlalchemy as sa

# create metadata object
metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

# define table object
vpl = sa.Table('view_primary_log', metadata, autoload=True)

# query parameters
meter_name = 'ml03'
date_start = '20111015'
date_end = '20111201'
ip_mains = '192.168.1.200'

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

# graph
import pylab
pylab.plot_date(dates,watthours,'ko-')
pylab.grid()
pylab.show()

