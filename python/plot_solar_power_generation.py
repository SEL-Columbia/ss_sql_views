'''
plot_solar_power_generation.py
==============================
this script plots the hourly solar power generated
'''
import datetime as dt
date_start = dt.datetime(2011, 12, 01)
date_end   = dt.datetime(2011, 12, 31)
meter_name = 'ug03'


def plot_solar_power_generation():
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    vsp = sa.Table('view_solar_power', metadata, autoload=True)

    query = sa.select([vsp.c.meter_timestamp, vsp.c.power],
                      distinct=True,
                      order_by=vsp.c.meter_timestamp,
                      whereclause=sa.and_(vsp.c.meter_name==meter_name,
                                       vsp.c.meter_timestamp>date_start,
                                       vsp.c.meter_timestamp<date_end)
                      )
    print query

    # get list of meter names in solar logs
    meter_timestamp = []
    power = []
    result = query.execute()
    for r in result:
        print r
        meter_timestamp.append(r.meter_timestamp)
        power.append(r.power)

    import matplotlib.pyplot as plt
    f, ax = plt.subplots(1,1)
    ax.plot_date(meter_timestamp, power)
    plt.show()

if __name__ == '__main__':
    plot_solar_power_generation()