'''
solar_generation.py
===================
this script fits a line to the solar kwh data to determine
the average daily kwh performance of the solar panel system

it also plots the cumulative kwh performance and the fit line.
'''

import datetime as dt
date_start = dt.datetime(2011, 12, 1)
date_end   = dt.datetime(2011, 12, 31)

def solar_generation():
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    vs = sa.Table('view_solar', metadata, autoload=True)

    query = sa.select([vs.c.meter_name], distinct=True, order_by=vs.c.meter_name)
    print query

    # get list of meter names in solar logs
    meter_list = []
    result = query.execute()
    for r in result:
        meter_list.append(r.meter_name)

    import matplotlib.pyplot as plt
    f, ax = plt.subplots(len(meter_list), 1)

    for i, meter_name in enumerate(meter_list):
        # get data in date range

        query = sa.select([vs.c.meter_timestamp, vs.c.solar_kwh],
                           whereclause=sa.and_(vs.c.meter_name==meter_name,
                                               vs.c.meter_timestamp>date_start)
                          )

        # fit linear
        result = query.execute()
        meter_timestamp = []
        solar_kwh = []
        for r in result:
            meter_timestamp.append(r.meter_timestamp)
            solar_kwh.append(r.solar_kwh)

        import numpy as np
        meter_timestamp = np.array(meter_timestamp)
        solar_kwh = np.array(solar_kwh)


        # report slope, show graph
        ax[i].plot_date(meter_timestamp, solar_kwh)

        date_minimum = min(meter_timestamp)
        date_maximum = max(meter_timestamp)

        meter_timestamp = [(ms-date_minimum).total_seconds() for ms in meter_timestamp]
        p = np.polyfit(meter_timestamp, solar_kwh, 1)
        print meter_name, '%.1f' % (p[0] * 3600 * 24), 'kWh per day'
        fit_timebase = np.linspace(0, (date_maximum-date_minimum).total_seconds(), 10)
        fit_energy = np.polyval(p, fit_timebase)
        fit_timebase = [date_minimum + dt.timedelta(seconds=ft) for ft in fit_timebase]

        ax[i]. plot_date(fit_timebase, fit_energy, 'k')


    f.savefig('solar_generation.pdf')


if __name__ == '__main__':
    solar_generation()