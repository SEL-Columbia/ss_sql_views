'''
plot_customer_daily_energy.py
-----------------------------

Loops through all circuits and creates pdf of daily watthours and credit.

Watthours are calculated based on the midnight sample.  This has a main
weakness due to the watthour reset bug.

Also includes linear fit to gauge if energy use is increasing over time.

'''

import sqlalchemy as sa
import matplotlib.pyplot as plt
import datetime as dt

date_start = dt.datetime(2011, 9, 1)
date_end = dt.datetime(2012, 2, 1)

def plot_customer_daily_energy():
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')
    vm = sa.Table('view_meter', metadata, autoload=True )

    method = 'no_reset'

    vmid = sa.Table('view_midnight', metadata, autoload=True)
    vp = sa.Table('view_power_table', metadata, autoload=True)

    # get list of circuits
    query = sa.select([vm.c.circuit_id,
                       vm.c.meter_name,
                       vm.c.ip_address],
                       order_by=(vm.c.meter_name, vm.c.ip_address),
                       #limit=3
                       )
    result = query.execute()
    circuit_list = []
    for r in result:
        circuit_list.append((r.circuit_id, r.meter_name, r.ip_address))

    # iterate over list of circuits
    for c in circuit_list:
        filename = 'pcde-' + c[1] + '-' + c[2][-3:] + '.pdf'
        query = sa.select([vmid.c.watthours,
                           vmid.c.credit,
                           vmid.c.meter_timestamp],
                           whereclause=sa.and_(vmid.c.circuit_id==c[0],
                                               vmid.c.meter_timestamp<date_end,
                                               vmid.c.meter_timestamp>date_start#,
                                               #vmid.c.watthours>0
                                               ),
                           order_by=vmid.c.meter_timestamp)

        if method == 'no_reset':
            query = sa.select([vp.c.watthours,
                               vp.c.credit,
                               vp.c.meter_timestamp],
                               whereclause=sa.and_(vp.c.circuit_id==c[0],
                                                   vp.c.meter_timestamp<date_end,
                                                   vp.c.meter_timestamp>date_start,
                                                   vp.c.watthours>0,
                                                   vp.c.power>=0,
                                                   vp.c.time_difference=='01:00:00',
                                                   sa.extract('hour',vp.c.meter_timestamp)==0),
                                order_by=vp.c.meter_timestamp)

        result = query.execute()
        dates = []
        watthours = []
        credit = []
        for r in result:
            dates.append(r.meter_timestamp)
            watthours.append(r.watthours)
            credit.append(r.credit)

        if len(dates) == 0:
            continue

        # plot each circuit daily energy values for all time
        f, ax = plt.subplots(2,1, sharex=True)


        # fit linear slope to watthour data
        import numpy as np
        dates = np.array(dates)
        watthours = np.array(watthours)

        date_max = max(dates)
        date_min = min(dates)

        # convert dates to seconds with t=0 as first sample
        meter_timestamp = [(d-date_min).total_seconds() for d in dates]
        p = np.polyfit(meter_timestamp, watthours, 1)
        output_string = '%.3f kWh per day' % (p[0] * 3600 * 24)
        #print output_string#'%.1f' % (p[0] * 3600 * 24), 'kWh per day'
        print str(c[0]) + ',' + str(c[1]) + ',' + str(c[2]) + ',',
        print ('%.1f' % watthours.mean()) + ',',
        print ('%.3f' % (p[0] * 3600 * 24)) + ',',
        print len(dates)
        ax[0].text(0.05, 0.7, output_string, transform=ax[0].transAxes)
        fit_timebase = np.linspace(0, (date_max - date_min).total_seconds(), 10)
        fit_energy = np.polyval(p, fit_timebase)
        fit_timebase = [date_min + dt.timedelta(seconds=ft) for ft in fit_timebase]
        ax[0].plot_date(fit_timebase, fit_energy, 'k')
        #ax[0].legend()


        ax[0].plot_date(dates, watthours, mfc='#dddddd')
        ax[0].set_xlabel('Date')
        ax[0].set_ylabel('Daily Watthours')
        ax[0].set_xlim((date_start, date_end))
        ax[0].set_title(filename)
        ax[1].plot_date(dates, credit, mfc='#dddddd', linestyle='-', color='k')
        ax[1].set_ylabel('Credit at Midnight')
        f.autofmt_xdate()
        f.savefig(filename)
        plt.close()

if __name__ == '__main__':
    plot_customer_daily_energy()
