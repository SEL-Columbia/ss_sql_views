'''
customer_energy_histogram.py
============================

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
    for cd in circuit_dict_list:
        #print 'querying'
        if cd['meter_name'] not in meter_list:
            continue
        num_circuits += 1
        print num_circuits
        de = get_daily_energy_for_circuit_id(cd['circuit_id'], date_start, date_end)
        if de == None:
            continue
        #de.values.astype(float)
        all_energy = np.hstack((all_energy, de.values))

        # append de.values to all_energy
    #1/0

    if remove_zeros:
        all_energy = all_energy[all_energy > 0]
    # concatenate

    # plot histogram
    import matplotlib.pyplot as plt
    f = plt.figure()
    ax = f.add_axes((0.2,0.3,0.6,0.6))
    #import numpy as np
    #ax.hist(watthour_list, bins=np.linspace(0,4000,41), facecolor='#dddddd')
    ax.hist(all_energy, bins=np.linspace(0,200,41), facecolor='#dddddd', normed=True)
    #ax.hist(watthour_list)
    ax.set_xlabel('Daily Electrical Energy Consumed (Wh)')
    ax.set_ylabel('Frequency of Observation')

    # add annotations to plot
    annotation = []
    annotation.append('plot generated ' + str(dt.datetime.now()))
    annotation.append('date start = ' + str(date_start))
    annotation.append('date end = ' + str(date_end))
    annotation.append('meter list = ' + str(meter_list))
    annotation = '\n'.join(annotation)
    f.text(0.01,0.01, annotation)

    if title != None:
        ax.set_title(title)
    f.savefig(filename)

    print 'number of datapoints = ', len(all_energy)
    print 'possible observations = ', num_circuits * (date_end - date_start).days

if __name__ == '__main__':
    plot_customer_energy_histogram()