'''
consumer_credit_histogram.py
============================

note: if consumer has only zero credit, they are dropped from analysis
'''

from __future__ import division

import datetime as dt

date_start = dt.datetime(2011, 9, 01)
date_end   = dt.datetime(2012, 01, 01)
figure_file_name = 'percentage_with_credit.pdf'
mains_ip = '192.168.1.200'
meter_name = ('ml01', 'ml02', 'ml03', 'ml04', 'ml05', 'ml06', 'ml07', 'ml08')

def consumer_credit_histogram(date_start, date_end, axes):
    #def percentage_with_credit():
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    vpl = sa.Table('view_primary_log', metadata, autoload=True)
    vm = sa.Table('view_midnight', metadata, autoload=True)


    print 'executing non-zero hours query'
    # count number of hours per circuit with credit greater than zero
    query = sa.select([vpl.c.circuit_id,
                       sa.func.count(vpl.c.circuit_id).over(partition_by=vpl.c.circuit_id).label('count')],
                       whereclause=sa.and_(vpl.c.credit>0,
                                           vpl.c.meter_timestamp>date_start,
                                           vpl.c.meter_timestamp<date_end,
                                           vpl.c.meter_name.in_(meter_name),
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
                                           vpl.c.meter_name.in_(meter_name),
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

    if nzdk==thdk:
        print 'circuits match'
    else:
        print 'circuits do not match'

    circuits = nzdk.intersection(thdk)

    percentage_with_credit = []
    for c in circuits:
        percentage_with_credit.append(non_zero_hours_dict[c] / total_hours_dict[c])


    axes.hist(percentage_with_credit,
              bins=np.arange(0, 1.1, 0.1),
              cumulative=True,
              normed=True
              )
    axes.set_title(str(date_start) + ' - ' + str(date_end))
    axes.set_xlabel('Percentage of Time With Credit Available')
    axes.set_ylabel('Number of Customers')
    axes.grid(True)
    #ax.set_xlabel('Average Daily Energy Use (Wh)')
    #ax.set_ylabel('Fraction of Time with Credit Available')

    #f.savefig(figure_file_name)

if __name__ == '__main__':

    multiple = True

    import numpy as np
    import matplotlib.pyplot as plt

    if multiple:
        f, ax = plt.subplots(4,1, sharey=True, figsize=(8,20))
    else:
        f, ax = plt.subplots(1,1)

        date_start = dt.datetime(2011, 9, 01)
        date_end   = dt.datetime(2011, 10, 01)

        consumer_credit_histogram(date_start=date_start,
                               date_end=date_end,
                               axes=ax)
    if multiple == True:
        date_start = dt.datetime(2011, 9, 01)
        date_end   = dt.datetime(2011, 10, 01)

        consumer_credit_histogram(date_start=date_start,
                               date_end=date_end,
                               axes=ax[0])

        date_start = dt.datetime(2011, 10, 01)
        date_end   = dt.datetime(2011, 11, 01)

        consumer_credit_histogram(date_start=date_start,
                               date_end=date_end,
                               axes=ax[1])

        date_start = dt.datetime(2011, 11, 01)
        date_end   = dt.datetime(2011, 12, 01)

        consumer_credit_histogram(date_start=date_start,
                               date_end=date_end,
                               axes=ax[2])

        date_start = dt.datetime(2011, 12, 01)
        date_end   = dt.datetime(2012,  1, 01)

        consumer_credit_histogram(date_start=date_start,
                               date_end=date_end,
                               axes=ax[3])


    #plt.show()
    f.savefig('credit_histogram.pdf')