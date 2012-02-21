'''
plot_customer_hourly_power_profile.py
-----------------------------
PCHP

get full list of energy on an hourly basis from view_primary_log

use pandas to do a one hour time lag

plot hourly power overlaid



'''

import sqlalchemy as sa
import matplotlib.pyplot as plt
import datetime as dt

date_start = dt.datetime(2012, 1, 1)
date_end = dt.datetime(2012, 2, 20)

if __name__ == '__main__':

    import offline_gateway as og
    circuit_list = og.get_circuit_list()

    debug = False
    #debug = True
    if debug:
        circuit_list = circuit_list[:2]



    # iterate over list of circuits
    for c in circuit_list:
        filename = 'pchpp-' + c[1] + '-' + c[2][-3:] + '.pdf'
        print 'querying for', filename

        import offline_gateway as og
        df = og.get_watthours_for_circuit_id(c[0], date_start, date_end)

        # offset by 1 hour
        import pandas as p
        offset = df - df.shift(1, offset=p.DateOffset(hours=1))

        positive_only = True
        if positive_only:
            offset = offset[offset.values >= 0]


        hour = [ind.hour for ind in offset.index]

        #1/0

        # iterate over series and plot hour, value as pairs
        # or create two lists from series

        # plot each circuit daily energy values for all time
        f, ax = plt.subplots(1, 1, sharex=True)

        ax.plot(hour, offset.values, linestyle='',
                marker='o', mec='#ffffff', alpha=0.2, mfc=None)
        ax.set_xlabel('Date')
        ax.set_ylabel('Average Hourly Power')
        #ax.set_xlim((date_start, date_end))
        ax.set_title(filename)
        f.autofmt_xdate()
        f.savefig(filename)
        plt.close()
