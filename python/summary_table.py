'''
summary_table.py
----------------


'''

def query_midnight_watthours_by_meter(date_start, date_end, meter_name):
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    vm = sa.Table('view_midnight', metadata, autoload=True)

    # get meter list from database
    query = sa.select([vm.c.ip_address,
                       sa.func.avg(vm.c.watthours).over(partition_by=vm.c.circuit_id).label('myavg'),
                       sa.func.max(vm.c.watthours).over(partition_by=vm.c.circuit_id).label('mymax'),
                       sa.func.count(vm.c.watthours).over(partition_by=vm.c.circuit_id).label('mycount')
                       ],
                       whereclause=sa.and_(vm.c.watthours>0,
                                           vm.c.meter_timestamp>date_start,
                                           vm.c.meter_timestamp<date_end,
                                           vm.c.meter_name==meter_name
                       ),
                       distinct=True,
                       )
    return query

def query_max_power(date_start, date_end, meter_name):
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    vp = sa.Table('view_power', metadata, autoload=True)

    # get meter list from database
    query = sa.select([vp.c.ip_address,
                       sa.func.max(vp.c.power).over(partition_by=vp.c.circuit_id).label('max_power')],
                       whereclause=sa.and_(vp.c.meter_timestamp>date_start,
                                           vp.c.meter_timestamp<date_end,
                                           vp.c.meter_name==meter_name
                       ),
                       distinct=True,
                       )
    return query


import datetime as dt
date_start = dt.datetime(2012,01,01)
date_end = dt.datetime(2012,02,01)
meter_name = 'ug08'
columns = ('avg_energy', 'days_reporting', 'max_energy', 'max_power')


# avg, max, days_reporting query
query = query_midnight_watthours_by_meter(date_start=date_start,
                                          date_end=date_end,
                                          meter_name=meter_name)

result = query.execute()
data = {}
for r in result:
    if r.ip_address not in data.keys():
        data[r.ip_address] = {}
    data[r.ip_address]['avg_energy']='%.1f' % r.myavg
    data[r.ip_address]['max_energy']=r.mymax
    data[r.ip_address]['days_reporting']=r.mycount


# max_power query
query = query_max_power(date_start=date_start,
                        date_end=date_end,
                        meter_name=meter_name)
result = query.execute()
for r in result:
    if r.ip_address not in data.keys():
        data[r.ip_address] = {}
    data[r.ip_address]['max_power']=r.max_power


# output data in table
print 'meter name =', meter_name
print 'start date =', date_start
print 'end date =', date_end

keys = data.keys()
keys.sort()

print 'key',
print columns
for key in keys:
    print key,
    for col in columns:
        if col in data[key].keys():
            print str(data[key][col]).rjust(10),
        else:
            print '-'.rjust(10),
    print
