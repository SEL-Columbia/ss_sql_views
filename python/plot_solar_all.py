'''
plot_solar_all.py
-----------------------------
at a glance plot with solar kwh, battery voltage, solar power
'''

import sqlalchemy as sa
import matplotlib.pyplot as plt
import datetime as dt

date_start = dt.datetime(2012, 2, 15)
date_end = dt.datetime(2012, 3, 15)

meter_list = ['ml00', 'ml01', 'ml02', 'ml03', 'ml04', 'ml05', 'ml06', 'ml07', 'ml08',
              'ug01', 'ug02', 'ug03', 'ug04', 'ug05', 'ug06', 'ug07', 'ug08']


if __name__ == '__main__':

    import offline_gateway as og

    for i, meter_name in enumerate(meter_list):

        filename = 'psa-' + meter_name + '.pdf'
        print 'querying for ' + filename


        # plot each circuit daily energy values for all time
        f, ax = plt.subplots(4, 1, sharex=True, figsize=(8,12))

        # plot hourly_kwh on axis 0
        hourly_kwh = og.get_solar_kwh_for_meter_name(meter_name, date_start, date_end)
        if hourly_kwh == None:
            continue

        ax[0].plot_date(hourly_kwh.index, hourly_kwh.values, 'ko-')
        #ax[0].set_xlabel('Date')
        ax[0].set_ylabel('Delivered Energy (kWh)')
        ax[0].set_xlim((date_start, date_end))
        #ax[0].set_title(filename)

        # plot battery_voltage on axis 1
        battery_voltage = og.get_battery_voltage_for_meter_name(meter_name, date_start, date_end)
        ax[1].plot_date(battery_voltage.index, battery_voltage.values, 'ko-')
        ax[1].set_ylabel('Battery Voltage (V)')



        '''
        # calculate hourly power/energy
        import pandas as p
        hourly_power = hourly_energy.shift(-1, offset=p.DateOffset(hours=1)) - hourly_energy

        ax[2].plot_date(hourly_power.index, hourly_power.values, 'ko')
        ax[2].set_ylabel('Average Power (W)')

        # plot daily energy
        daily_energy_nr = og.get_daily_energy_for_circuit_id_nr(c['circuit_id'], date_start, date_end)

        ax[3].plot_date(daily_energy_nr.index, daily_energy_nr.values, 'ko')
        ax[3].set_ylabel('Daily Energy (Wh)')
        '''

        #plt.show()
        f.autofmt_xdate()
        f.savefig(filename)
        plt.close()

