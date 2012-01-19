'''
which_meters_reporting_CSV.py
==============================

this script provides a CSV output of number of circuits reporting
for each meter for each time period.

to output directly to file::

    python which_meters_reporting_CSV.py > filename.csv

'''

from __future__ import division

import datetime as dt
date_start = dt.datetime(2011, 12, 01)
date_end = dt.datetime(2011, 12, 03)

def which_meters_reporting_CSV():
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    vpl = sa.Table('view_primary_log', metadata, autoload=True)
    vm = sa.Table('view_meter', metadata, autoload=True)

    # get list of meters and number of circuits on each meter from database
    query = sa.select([vm.c.meter_name,
                       sa.func.count(vm.c.circuit_id).label('num_circuits')],
                       group_by=vm.c.meter_name)
    result = query.execute()
    meter_dict = {}
    for r in result:
        meter_dict[r.meter_name]=r.num_circuits

    # print header line of CSV output
    print 'date,',
    sorted_keys = meter_dict.keys()
    sorted_keys.sort()
    for k in sorted_keys:
        print k + ',',
    print

    # loop over time period date_start -> date_end
    this_start = date_start
    while 1:
        this_end = this_start + dt.timedelta(hours=1)

        # query database for number of reports grouping by meter
        query = sa.select([sa.func.count(vpl.c.watthours).label('num_circuits'),
                           vpl.c.meter_name],
                           whereclause=sa.and_(vpl.c.meter_timestamp >= this_start,
                                               vpl.c.meter_timestamp < this_end),
                           group_by=vpl.c.meter_name,
                           order_by=vpl.c.meter_name)
        result = query.execute()
        result_dict = {}
        for r in result:
            result_dict[r.meter_name] = r.num_circuits

        # print out csv row
        print str(this_start) + ',',
        for m in sorted_keys:
            if m in result_dict.keys():
                print ('%.2f' % (result_dict[m]/meter_dict[m])).rjust(4) + ',',
            else:
                print '0.00'.rjust(4) + ',',
        print

        # increment dates
        this_start = this_end
        if this_start >= date_end:
            break

if __name__ == '__main__':
    which_meters_reporting_CSV()