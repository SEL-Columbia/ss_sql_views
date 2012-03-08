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
        og.plot_solar_all(meter_name, date_start, date_end)

