'''
plot_customer_daily_energy.py
-----------------------------

Loops through all circuits and creates pdf of daily watthours.

Watthours are calculated based on the midnight sample.

'''

import sqlalchemy as sa
import matplotlib.pyplot as plt
import datetime as dt

date_end = '2012-02-02'

metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')
vm = sa.Table('view_meter', metadata, autoload=True )
vmid = sa.Table('view_midnight', metadata, autoload=True)

query = sa.select([vm.c.circuit_id,
                   vm.c.meter_name,
                   vm.c.ip_address],
                   order_by=(vm.c.meter_name, vm.c.ip_address))
result = query.execute()
circuit_list = []
for r in result:
    circuit_list.append((r.circuit_id, r.meter_name, r.ip_address))

for c in circuit_list:
    print c
    filename = 'pcde-' + c[1] + '-' + c[2][-3:] + '.pdf'
    query = sa.select([vmid.c.watthours,
                       vmid.c.meter_timestamp],
                       whereclause=sa.and_(vmid.c.circuit_id==c[0],
                                           vmid.c.meter_timestamp<date_end),
                       order_by=vmid.c.meter_timestamp)
    result = query.execute()
    dates = []
    watthours = []
    for r in result:
        dates.append(r.meter_timestamp)
        watthours.append(r.watthours)
    f, ax = plt.subplots(1,1)
    ax.plot_date(dates, watthours)
    ax.set_xlabel('Date')
    ax.set_ylabel('Daily Watthours')
    ax.set_title(filename)
    f.savefig(filename)
    plt.close()


# iterate over list of circuits
# plot each circuit daily energy values for all time
# save under filename meter_name_ip_address.pdf

