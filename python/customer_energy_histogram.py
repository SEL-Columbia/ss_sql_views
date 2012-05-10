'''
customer_energy_histogram.py
============================
outputs
-------
a histogram displaying the frequency of customer daily energy values for
a list of meters.

inputs
------
meter_list : list of strings describing meter_name identifier in database
date_start : datetime object that describes start of data
date_end   : datetime object that describes end of data
filename   : string specifying name of output file
annotate   : boolean for output annotation on plot
remove_zeros : boolean to control removal of zero consumption from histogram
title : string that will be used as title for plot
'''

from offline_gateway import *
import datetime as dt
import pandas as p
import numpy as np

def plot_customer_energy_histogram(meter_list=['ml01', 'ml02', 'ml03', 'ml04', 'ml05', 'ml06', 'ml07', 'ml08'],
                                   date_start=dt.datetime(2012, 1, 1),
                                   date_end=dt.datetime(2012, 2, 1),
                                   filename='default_histogram.pdf',
                                   annotate=False,
                                   remove_zeros=True,
                                   title=None):

    # select all circuits from database (we will later filter)
    circuit_dict_list = get_circuit_dict_list(mains=False)

    # get daily energy for each circuit
    all_energy = p.Series()
    all_energy = np.array([])
    num_circuits = 0

    # iterate over circuit_dict_list and skip meters not in meter_list
    for cd in circuit_dict_list:
        if cd['meter_name'] not in meter_list:
            continue
        print cd['circuit_id']
        num_circuits += 1
        de, err = get_daily_energy_for_circuit_id(cd['circuit_id'], date_start, date_end)
        if err != 0:
            continue
        all_energy = np.hstack((all_energy, de.values))

    # remove any days of zero consumption from array and histogram
    if remove_zeros:
        all_energy = all_energy[all_energy > 0]

    # plot histogram
    import matplotlib.pyplot as plt
    f = plt.figure()

    # set plot boundary appropriately to make room for annotation
    if annotate:
        ax = f.add_axes((0.2,0.3,0.6,0.6))
    else:
        ax = f.add_axes((0.1, 0.1, 0.85, 0.8))

    # plot and set labels
    ax.hist(all_energy, bins=np.linspace(0,200,41), facecolor='#dddddd', normed=True)
    ax.set_xlabel('Daily Electrical Energy Consumed (Wh)')
    ax.set_ylabel('Frequency of Observation')
    if title != None:
        ax.set_title(title)

    # create metadata and plot to stdout
    annotation = []
    annotation.append('plot generated ' + str(dt.datetime.now()))
    annotation.append('date start = ' + str(date_start))
    annotation.append('date end = ' + str(date_end))
    annotation.append('meter list = ' + str(meter_list))
    annotation = '\n'.join(annotation)
    print annotation
    print 'number of datapoints = ', len(all_energy)
    print 'possible observations = ', num_circuits * (date_end - date_start).days

    # add metadata to plot
    if annotate:
        f.text(0.01, 0.01, annotation)

    # save to file
    f.savefig(filename)


if __name__ == '__main__':

    plot_customer_energy_histogram(meter_list=['ml01', 'ml02', 'ml03', 'ml04', 'ml05', 'ml06', 'ml07', 'ml08'],
                                   title='Mali Customer Daily Energy Histogram',
                                   filename='Mali_Histogram.pdf')
    '''
    plot_customer_energy_histogram(meter_list=['ug01', 'ug02', 'ug03', 'ug04', 'ug05', 'ug06', 'ug07', 'ug08'],
                                   title='Uganda Customer Daily Energy Histogram',
                                   filename='Uganda_Histogram.pdf')
    '''