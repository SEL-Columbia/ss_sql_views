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

if __name__ == '__main__':

    import offline_gateway as og
    cdl = og.get_circuit_dict_list(mains=True)
    #cdl = cdl[:2]

    for i, c in enumerate(cdl):

        filename = 'pcde-' + c['meter_name'] + '-' + c['ip_address'][-3:] + '.pdf'
        print 'querying for' + filename
        daily_energy = og.get_daily_energy_for_circuit_id(c['circuit_id'], date_start, date_end)

        # plot each circuit daily energy values for all time
        f, ax = plt.subplots(2, 1, sharex=True)

        '''
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
        '''

        ax[0].plot_date(daily_energy.index, daily_energy.values, mfc='#dddddd')
        ax[0].set_xlabel('Date')
        ax[0].set_ylabel('Daily Watthours')
        ax[0].set_xlim((date_start, date_end))
        ax[0].set_title(filename)

        f.autofmt_xdate()
        f.savefig(filename)
        plt.close()

