'''
meter_parasitics_power.py
-------------------------



'''

# query parameters
import numpy as np
import datetime as dt
date_start = dt.datetime(2011, 10, 10)
date_end   = dt.datetime(2011, 10, 15)
ip_mains = '192.168.1.200'
figure_title = 'Hourly Meter Parasitic Power'
figure_filename = 'meter_parasitics_power.pdf'
filter_zeros = True

meter_list = ('ml03','ml03')

def aggregated_customer_energy():
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    #vpl = sa.Table('view_primary_log', metadata, autoload=True)
    vp = sa.Table('view_power', metadata, autoload=True)
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


    meter_list = ('ml03','ml04')
    print 'meters being reported are ', meter_list

    # graph
    import pylab
    import matplotlib.pyplot as plt
    import math
    f, ax = plt.subplots(len(meter_list), 1, sharex=True)
    f.set_size_inches((16, 16))
    for i, meter_name in enumerate(meter_list):
        print 'querying for meter', meter_name
        # sum will show up with key 'sum_1'
        query = sa.select([sa.func.sum(vp.c.power).label('customer_sum'),
                           vp.c.meter_timestamp],
                          whereclause=sa.and_(vp.c.meter_name == meter_name,
                                              vp.c.meter_timestamp > date_start,
                                              vp.c.meter_timestamp < date_end,
                                              vp.c.ip_address != ip_mains),
                          group_by=vp.c.meter_timestamp,
                          order_by=vp.c.meter_timestamp)
        result = query.execute()

        # parse result into arrays
        agg_dates = []
        agg_watthours = []
        for r in result:
            agg_watthours.append(r.customer_sum)
            agg_dates.append(r.meter_timestamp)

        # query for MAINS consumption
        # sum is unnecessary but i'll leave it for now
        query = sa.select([sa.func.sum(vp.c.power).label('mains_power'), vp.c.meter_timestamp],
                          whereclause=sa.and_(vp.c.meter_name == meter_name,
                                              vp.c.meter_timestamp > date_start,
                                              vp.c.meter_timestamp < date_end,
                                              vp.c.ip_address == ip_mains),
                          group_by=vp.c.meter_timestamp,
                          order_by=vp.c.meter_timestamp)
        result = query.execute()

        # parse result into arrays
        main_dates = []
        main_watthours = []
        for r in result:
            main_watthours.append(r.mains_power)
            main_dates.append(r.meter_timestamp)

        if main_dates == agg_dates:
            print 'dates equal'
        else:
            print 'dates not equal'

        # cast lists as sets, get union
        common_dates = set(main_dates).intersection(set(agg_dates))

        # take watthours from array where dates = common_dates
        parasitic_watthours = []
        for date in common_dates:
            parasitic_watthours.append(main_watthours[main_dates.index(date)] -
                                       agg_watthours[agg_dates.index(date)])



        ax[i].plot_date(main_dates, parasitic_watthours, 'ko-', label=meter_name)
        ax[i].set_xlim((date_start, date_end))
        ax[i].set_ylim((0,250))
        #ax[i].set_yticks((0,500,1000,1500))
        ax[i].legend(loc=[1,0])
        ax[i].grid(True)

    #plt.show()
    f.suptitle(figure_title)
    f.savefig(figure_filename)

if __name__=='__main__':
    aggregated_customer_energy()