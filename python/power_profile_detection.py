'''
power_profile_detection.py
-----------------------------

plot each hourly profile as separate trace


'''

import sqlalchemy as sa
import matplotlib.pyplot as plt
import datetime as dt

date_start = dt.datetime(2011, 9,  1)
date_end   = dt.datetime(2012, 2, 27)

if __name__ == '__main__':

    import offline_gateway as og
    cdl = og.get_circuit_dict_list()

    debug = False
    #debug = True
    if debug:
        cdl = cdl[34:36]

    # iterate over list of circuits
    for c in cdl:

        if c['meter_name'] != 'ml05':
            continue
        # query for watthours
        filename = 'ppd-' + c['meter_name'] + '-' + c['ip_address'][-3:] + '.pdf'
        print 'querying for', filename
        import offline_gateway as og
        df = og.get_watthours_for_circuit_id(c['circuit_id'], date_start, date_end)

        if df == None:
            continue

        # offset by 1 hour and subtract
        import pandas as p
        offset = df.shift(-1, offset=p.DateOffset(hours=1)) - df

        if len(offset) == 0:
            continue

        # screen out negative values resulting from drops
        positive_only = True
        if positive_only:
            offset = offset[offset.values >= 0]

        if len(offset) == 0:
            continue

        # extract hour information from series index for plotting
        import numpy as np
        hour = np.array([ind.hour for ind in offset.index])

        #1/0
        # plotting of hour vs. power values to create profile
        #f = plt.figure()
        #ax = f.add_axes((0.2,0.2,0.6,0.6))
        f, ax = plt.subplots(24, 1, figsize=(8,20))

        for this_hour in range(24):

            #1/0
            mask = hour == this_hour

            dates = offset.index[mask]
            power = offset.values[mask]

            if len(dates) == 0:
                continue
            #print offset.index[hour==this_hour]
            #print offset.values[hour==this_hour]
            ax[this_hour].plot(offset.index[hour==this_hour],
                         offset.values[hour==this_hour],
                         'ko')

        #ax.legend()
        #ax.set_xlabel('Hour of Day')
        #ax.set_ylabel('Average Hourly Power (W)')
        #ax.set_xticks((0,4,8,12,16,20,24))
        #ax.set_xlim((-1, 25))
        #ax.set_title(filename)

        # add annotations to plot
        annotation = []
        annotation.append('plot generated ' + str(dt.datetime.now()))
        annotation.append('date start = ' + str(date_start))
        annotation.append('date end = ' + str(date_end))
        annotation = '\n'.join(annotation)
        f.text(0.01,0.01, annotation)

        # save to file
        f.savefig(filename, transparent=True)
        #plt.show()
        plt.close()
