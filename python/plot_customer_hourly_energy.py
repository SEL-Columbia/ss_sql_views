'''
plot_customer_hourly_energy.py
-----------------------------

Loops through all circuits and creates pdf of daily watthours and credit.

Watthours are calculated based on the midnight sample.  This has a main
weakness due to the watthour reset bug.

Also includes linear fit to gauge if energy use is increasing over time.

'''

import sqlalchemy as sa
import matplotlib.pyplot as plt
import datetime as dt

date_start = dt.datetime(2012, 2, 14)
date_end = dt.datetime(2012, 2, 20)

def get_circuit_list():
    import sqlalchemy as sa
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')
    vm = sa.Table('view_meter', metadata, autoload=True )
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
    return circuit_list


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

if __name__ == '__main__':
    plot_customer_hourly_energy()
