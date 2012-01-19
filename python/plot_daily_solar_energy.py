'''
plot_daily_solar_energy.py
==============================
uses the midnight values of the reported cumulative kWh to generate
a daily report of energy delivered to the battery

only reports on days where there are two consecutive readings

right now uses numpy to do differentiation, should use postgres lag instead

'''

import datetime as dt
date_start = dt.datetime(2011, 11, 01)
date_end   = dt.datetime(2012, 12, 31)
meter_name = 'ml05'


def plot_solar_power_generation():
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    vspm = sa.Table('view_solar_midnight', metadata, autoload=True)

    query = sa.select([vspm.c.meter_timestamp, vspm.c.solar_kwh],
                      distinct=True,
                      order_by=vspm.c.meter_timestamp,
                      whereclause=sa.and_(vspm.c.meter_name==meter_name,
                                       vspm.c.meter_timestamp>date_start,
                                       vspm.c.meter_timestamp<date_end)
                      )
    print query

    # get list of meter names in solar logs
    meter_timestamp = []
    solar_kwh = []
    result = query.execute()
    for r in result:
        print r
        meter_timestamp.append(r.meter_timestamp)
        solar_kwh.append(r.solar_kwh)

    import numpy as np
    meter_timestamp = np.array(meter_timestamp)
    solar_kwh = np.array(solar_kwh)
    solar_kwh_per_day = np.diff(solar_kwh)

    td = np.diff(meter_timestamp)
    meter_timestamp= meter_timestamp[td==dt.timedelta(days=1)]
    solar_kwh = solar_kwh_per_day[td==dt.timedelta(days=1)]

    import matplotlib.pyplot as plt
    f, ax = plt.subplots(1,1)
    ax.plot_date(meter_timestamp, solar_kwh)
    plt.show()

if __name__ == '__main__':
    plot_solar_power_generation()