'''
percentage_with_credit.py
=========================
Determines for what fraction of reporting hours customers have credit greater than zero.

Performs query for number of hours reporting with credit above zero.  Performs a second
query with number of hours reporting total for each circuit.

Modeled after Figure 11 in the ICTD 2012 paper.

Note: does not catch zero usage.

'''

from __future__ import division

import datetime as dt

date_start = dt.datetime(2011, 12, 01)
date_end   = dt.datetime(2012, 01, 01)
figure_file_name = 'percentage_with_credit.pdf'
mains_ip = '192.168.1.200'
meter_name = 'ug02'

def percentage_with_credit():
    #def percentage_with_credit():
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    vpl = sa.Table('view_primary_log', metadata, autoload=True)
    vm = sa.Table('view_midnight', metadata, autoload=True)

    print 'executing energy query'
    # get average daily from midnight table
    query = sa.select([vm.c.circuit_id,
                       sa.func.avg(vm.c.watthours).over(partition_by=vm.c.circuit_id).label('watthours')],
                       whereclause=sa.and_(vm.c.meter_timestamp>date_start,
                                           vm.c.meter_timestamp<date_end,
                                           vm.c.meter_name==meter_name,
                                           vm.c.ip_address!=mains_ip),
                       order_by=vm.c.circuit_id,
                       distinct=True)
    #print query
    result = query.execute()

    energy_dict = {}
    for r in result:
        energy_dict[r.circuit_id] = r.watthours

    # get set of keys from energy dict
    edk = set(energy_dict.keys())

    print 'executing non-zero hours query'
    # count number of hours per circuit with credit greater than zero
    query = sa.select([vpl.c.circuit_id,
                       sa.func.count(vpl.c.circuit_id).over(partition_by=vpl.c.circuit_id).label('count')],
                       whereclause=sa.and_(vpl.c.credit>0,
                                           vpl.c.meter_timestamp>date_start,
                                           vpl.c.meter_timestamp<date_end,
                                           vpl.c.meter_name==meter_name,
                                           vpl.c.ip_address!=mains_ip),
                       order_by=vpl.c.circuit_id,
                       distinct=True)
    #print query
    result = query.execute()

    circuit_ids = []
    hours_with_credit = []
    non_zero_hours_dict = {}
    for r in result:
        circuit_ids.append(r.circuit_id)
        hours_with_credit.append(r.count)
        non_zero_hours_dict[r.circuit_id] = r.count

    nzdk = set(non_zero_hours_dict.keys())

    print 'executing total hours query'
    # count number of hours per circuit reporting total
    query = sa.select([vpl.c.circuit_id,
                       sa.func.count(vpl.c.circuit_id).over(partition_by=vpl.c.circuit_id).label('count')],
                       whereclause=sa.and_(vpl.c.meter_timestamp>date_start,
                                           vpl.c.meter_timestamp<date_end,
                                           vpl.c.meter_name==meter_name,
                                           vpl.c.ip_address!=mains_ip),
                       order_by=vpl.c.circuit_id,
                       distinct=True)
    #print query
    result = query.execute()

    circuit_ids = []
    total_hours = []
    total_hours_dict = {}
    for r in result:
        circuit_ids.append(r.circuit_id)
        total_hours.append(r.count)
        total_hours_dict[r.circuit_id] = r.count

    thdk = set(total_hours_dict.keys())


    import numpy as np
    hours_with_credit = np.array(hours_with_credit)
    total_hours = np.array(total_hours)


    # create dictionary with circuits found in both queries
    print 'sym diff', nzdk.symmetric_difference(thdk)
    percentage_with_credit_dict = {}
    for k in nzdk.intersection(thdk):
        percentage_with_credit_dict[k] = non_zero_hours_dict[k] / total_hours_dict[k]
    pcdk = set(percentage_with_credit_dict.keys())

    import matplotlib.pyplot as plt
    f, ax = plt.subplots(1,1)

    # plot out pairs
    for k in edk.intersection(pcdk):
        print k, ',',
        print energy_dict[k], ',',
        print percentage_with_credit_dict[k]
        ax.plot(energy_dict[k], percentage_with_credit_dict[k], 'ko')

    ax.set_xlabel('Average Daily Energy Use (Wh)')
    ax.set_ylabel('Fraction of Time with Credit Available')

    f.savefig(figure_file_name)

if __name__ == '__main__':
    percentage_with_credit()