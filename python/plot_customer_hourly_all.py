'''
plot_customer_hourly_all.py
-----------------------------
at a glance plot with watthours, credit, hourly power, and daily energy
'''

import sqlalchemy as sa
import matplotlib.pyplot as plt
import datetime as dt

date_start = dt.datetime(2012, 3, 1)
date_end = dt.datetime(2012, 3, 28)


if __name__ == '__main__':

    import offline_gateway as og
    cdl = og.get_circuit_dict_list(mains=True)
    #cdl = cdl[:10]

    for i, c in enumerate(cdl):

        filename = 'pcha-' + c['meter_name'] + '-' + c['ip_address'][-3:] + '.pdf'
        print 'querying for ' + filename

        # grab hourly energy, if empty drop through loop
        hourly_energy, error = og.get_watthours_for_circuit_id(c['circuit_id'], date_start, date_end)
        #if hourly_energy == -1:
        if error != 0:
            continue

        # grab daily energy, if empty drop through loop
        daily_energy, error = og.get_daily_energy_for_circuit_id(c['circuit_id'], date_start, date_end)
        #if daily_energy == None:
        if error != 0:
            continue

        # shift daily_energy index by one to line up better
        import pandas as p
        daily_energy = daily_energy.shift(1, offset=p.DateOffset(days=1))

        # get hourly credit
        credit = og.get_credit_for_circuit_id(c['circuit_id'], date_start, date_end)

        # plot each circuit daily energy values for all time
        f, ax = plt.subplots(4, 1, sharex=True, figsize=(8,12))

        # plot energy on axis 0
        #ax[0].plot_date(daily_energy.index, daily_energy.values, mfc='#dddddd', ms=15)
        ax[0].plot_date(hourly_energy.index, hourly_energy.values, 'ko-')
        ax[0].set_xlabel('Date')
        ax[0].set_ylabel('Daily Watthours')
        ax[0].set_xlim((date_start, date_end))
        ax[0].set_title(filename)

        # plot credit on axis 1
        ax[1].plot_date(credit.index, credit.values, 'ko-')
        ax[1].set_ylabel('Credit Balance (XFCA)')


        # calculate hourly power/energy
        import pandas as p
        hourly_power = hourly_energy.shift(-1, offset=p.DateOffset(hours=1)) - hourly_energy

        ax[2].plot_date(hourly_power.index, hourly_power.values, 'ko')
        ax[2].set_ylabel('Average Power (W)')

        # plot daily energy
        daily_energy_nr, error = og.get_daily_energy_for_circuit_id_nr(c['circuit_id'], date_start, date_end)

        ax[3].plot_date(daily_energy_nr.index, daily_energy_nr.values, 'ko')
        ax[3].set_ylabel('Daily Energy (Wh)')


        #plt.show()
        f.autofmt_xdate()
        f.savefig(filename)
        plt.close()






def plot_customer_hourly_energy():
    import sqlalchemy as sa
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    circuit_list = get_circuit_list()

    #circuit_list = circuit_list[:2]

    t = sa.Table('view_primary_log', metadata, autoload=True)


    # iterate over list of circuits
    for c in circuit_list:
        filename = 'phde-' + c[1] + '-' + c[2][-3:] + '.pdf'
        print 'querying for', filename
        query = sa.select([t.c.watthours,
                           t.c.credit,
                           t.c.meter_timestamp],
                           whereclause=sa.and_(t.c.circuit_id==c[0],
                                               t.c.meter_timestamp<date_end,
                                               t.c.meter_timestamp>date_start),
                           order_by=t.c.meter_timestamp)


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
