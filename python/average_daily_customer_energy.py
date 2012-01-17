'''
calculates average energy ignoring zeros for every circuit and returns text dump
'''

import sqlalchemy as sa
import datetime as dt

date_start = dt.datetime(2010,12,1)
date_end = dt.datetime(2012,12,31)

# create metadata object
metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

# define table objects from database
vm = sa.Table('view_midnight', metadata, autoload=True)

# get meter list from database
query = sa.select([vm.c.meter_name,
                   vm.c.ip_address,
                   sa.func.avg(vm.c.watthours).over(partition_by=vm.c.circuit_id).label('myavg')
                   ],
                   whereclause=sa.and_(vm.c.watthours>0,
                                       vm.c.ip_address!='192.168.1.200',
                                       vm.c.meter_timestamp>date_start,
                                       vm.c.meter_timestamp<date_end
                   ),
                   distinct=True,
                   order_by=sa.desc('myavg')
                   )

print query
result = query.execute()

# print result
i=0
for r in result:
    print r.meter_name + '.' + r.ip_address[-3:] + '  %.1f' % r.myavg
    i+=1
