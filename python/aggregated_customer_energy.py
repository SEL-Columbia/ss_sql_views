'''
aggregated_customer_energy.py
------------------------------------
This script queries the database to return the aggregated consumer energy consumption
for each meter.

Each circuit that is not the mains has the hourly watthours added together and reported
in a timeseries chart.

In the header of the file are the configuration for dates and plot file name.

Note: The meter_list variable must also be changed (around line 42)

'''

# query parameters
import datetime as dt
date_start = dt.datetime(2011,01,01)
date_end = dt.datetime(2012,02,01)
ip_mains = '192.168.1.200'
figure_filename = 'all_customers.pdf'
filter_zeros = True

def aggregated_customer_energy():
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    #vpl = sa.Table('view_primary_log', metadata, autoload=True)
    vm = sa.Table('view_midnight', metadata, autoload=True)
    m = sa.Table('meter', metadata, autoload=True)

    # get meter list from database
    query = sa.select([m.c.name], order_by=m.c.name)
    result = query.execute()
    meter_list = []
    for r in result:
        meter_list.append(r.name)

    # prune meter list for mali or uganda
    #meter_list = meter_list[:9]
    #meter_list = meter_list[9:]
    print 'meters being reported are ', meter_list

    # graph
    import pylab
    import matplotlib.pyplot as plt
    import math
    f, ax = plt.subplots(len(meter_list), 1, sharex=True, sharey=True)
    f.set_size_inches((16, 16))
    for i, meter_name in enumerate(meter_list):
        # sum will show up with key 'sum_1'
        query = sa.select([sa.func.sum(vm.c.watthours), vm.c.meter_timestamp],
                          whereclause=sa.and_(vm.c.meter_name == meter_name,
                                              vm.c.meter_timestamp > date_start,
                                              vm.c.meter_timestamp < date_end,
                                              vm.c.ip_address != ip_mains),
                          group_by=vm.c.meter_timestamp,
                          order_by=vm.c.meter_timestamp)
        result = query.execute()

        # parse result into arrays
        dates = []
        watthours = []
        for r in result:
            watthours.append(r.sum_1)
            dates.append(r.meter_timestamp)

        # filter out any where sum is zero
        if filter_zeros:
            import numpy as np
            watthours = np.array(watthours)
            dates = np.array(dates)
            mask = watthours > 0
            watthours = watthours[mask]
            dates = dates[mask]

        ax[i].plot_date(dates,watthours,label=meter_name)
        ax[i].set_xlim((date_start, date_end))
        ax[i].set_yticks((0,500,1000,1500))
        ax[i].legend(loc=[1,0])
        ax[i].grid(True)

    #plt.show()
    f.suptitle('Aggregated Customer Watthours')
    f.savefig(figure_filename)

if __name__=='__main__':
    aggregated_customer_energy()