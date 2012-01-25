'''
loop over circuits and count resets occurring at 11pm instead of midnight.

use the view_power view as the base table.

if change from 11pm to midnight is zero or positive, count as correct

if change from 11pm to midnight is negative, count as incorrect

output meter_name, incorrect counts, correct counts

note: could speed up by close to a factor of two by doing a single query and then
using numpy to count positive/non-zero and negative values in array.
'''

import sqlalchemy as sa
import matplotlib.pyplot as plt
import datetime as dt

'''
returns list of dictionaries.  each list entry is a circuit.
'''
def get_list_of_circuits():
    query = sa.select([vm.c.circuit_id,
                       vm.c.meter_name,
                       vm.c.ip_address],
                       order_by=(vm.c.meter_name, vm.c.ip_address))
    result = query.execute()
    circuit_list = []
    for r in result:
        circuit_list.append({'circuit_id':r.circuit_id,
                             'meter_name':r.meter_name,
                             'ip_address':r.ip_address})
    return circuit_list


date_start = dt.datetime(2011, 12, 1)
date_end   = dt.datetime(2012,  2, 1)

metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')
vm = sa.Table('view_meter', metadata, autoload=True )
vp = sa.Table('view_power', metadata, autoload=True)

query = sa.select([vm.c.meter_name],
                   order_by=(vm.c.meter_name),
                   distinct=True)
result = query.execute()
meter_list = []
for r in result:
    meter_list.append(r.meter_name)

#print meter_list

# get list of circuits

result_list = []
for meter_name in meter_list:
    #print c
    query = sa.select([sa.func.count(vp.c.power).label('reset_count')],
                       whereclause=sa.and_(vp.c.meter_timestamp>date_start,
                                           vp.c.meter_timestamp<date_end,
                                           vp.c.meter_name==meter_name,
                                           vp.c.power<0,
                                           sa.extract('hour', vp.c.meter_timestamp)==0)
                     )
    result = query.execute()

    for r in result:
        print meter_name, r.reset_count,

    query2 = sa.select([sa.func.count(vp.c.power).label('reset_count')],
                       whereclause=sa.and_(vp.c.meter_timestamp>date_start,
                                           vp.c.meter_timestamp<date_end,
                                           vp.c.meter_name==meter_name,
                                           vp.c.power>=0,
                                           sa.extract('hour', vp.c.meter_timestamp)==0)
                     )
    result2 = query2.execute()
    for r in result2:
        print r.reset_count

