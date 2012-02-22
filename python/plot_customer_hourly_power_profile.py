'''
plot_customer_hourly_power_profile.py
-----------------------------
PCHPP

get full list of energy on an hourly basis from view_primary_log

use pandas to do a one hour time lag
power reported is over the hour

plot hourly power overlaid

warning: occasionally breaks due to:
ERROR: An unexpected error occurred while tokenizing input
The following traceback may be corrupted or invalid
The error message is: ('EOF in multi-line statement', (301, 0))
'''

import sqlalchemy as sa
import matplotlib.pyplot as plt
import datetime as dt

date_start = dt.datetime(2012, 1,  1)
date_end   = dt.datetime(2012, 2, 20)

if __name__ == '__main__':

    import offline_gateway as og
    cdl = og.get_circuit_dict_list()

    debug = False
    #debug = True
    if debug:
        cdl = cdl[:2]

    # iterate over list of circuits
    for c in cdl:

        # query for watthours
        filename = 'pchpp-' + c['meter_name'] + '-' + c['ip_address'][-3:] + '.pdf'
        print 'querying for', filename
        import offline_gateway as og
        df = og.get_watthours_for_circuit_id(c['circuit_id'], date_start, date_end)

        # offset by 1 hour and subtract
        import pandas as p
        offset = df.shift(-1, offset=p.DateOffset(hours=1)) - df

        # screen out negative values resulting from drops
        positive_only = True
        if positive_only:
            offset = offset[offset.values >= 0]

        # extract hour information from series index for plotting
        hour = [ind.hour for ind in offset.index]

        # plotting of hour vs. power values to create profile
        f = plt.figure()
        ax = f.add_axes((0.2,0.2,0.6,0.6))
        ax.plot(hour, offset.values, linestyle='',
                marker='o', mec='#ffffff', alpha=0.2, mfc=None)
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Average Hourly Power (W)')
        ax.set_xticks((0,4,8,12,16,20,24))
        ax.set_xlim((-1, 25))
        ax.set_title(filename)

        # add annotations to plot
        annotation = []
        annotation.append('plot generated ' + str(dt.datetime.now()))
        annotation.append('date start = ' + str(date_start))
        annotation.append('date end = ' + str(date_end))
        annotation = '\n'.join(annotation)
        f.text(0.01,0.01, annotation)

        # save to file
        f.savefig(filename, transparent=True)
        plt.close()
