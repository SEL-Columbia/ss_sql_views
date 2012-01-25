'''
plot_customer_daily_energy.py
-----------------------------

Loops through all circuits and creates pdf of daily watthours.

Watthours are calculated based on the midnight sample.

'''

import sqlalchemy as sa
import matplotlib.pyplot as plt
import datetime as dt

date_start = dt.datetime(2011, 1, 1)
date_end = dt.datetime(2012, 2, 1)

def plot_customer_daily_energy():
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')
    vm = sa.Table('view_meter', metadata, autoload=True )
    vmid = sa.Table('view_midnight', metadata, autoload=True)

    # get list of circuits
    query = sa.select([vm.c.circuit_id,
                       vm.c.meter_name,
                       vm.c.ip_address],
                       order_by=(vm.c.meter_name, vm.c.ip_address)#,
                       #limit=10
                       )
    result = query.execute()
    circuit_list = []
    for r in result:
        circuit_list.append((r.circuit_id, r.meter_name, r.ip_address))

    # iterate over list of circuits
    for c in circuit_list:
        print c
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
        result = query.execute()
        dates = []
        watthours = []
        credit = []
        for r in result:
            dates.append(r.meter_timestamp)
            watthours.append(r.watthours)
            credit.append(r.credit)
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
    plot_customer_daily_energy()
