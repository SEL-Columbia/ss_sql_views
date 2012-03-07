'''
customer_energy_histogram.py
============================
Creates a histogram of non-zero individual customer midnight samples over
a given date range and given country.
'''

#if __name__ == '__main__':
import offline_gateway as og

# get date range
import datetime as dt
date_start = dt.datetime(2012, 1, 1)
date_end = dt.datetime(2012, 2, 1)

# select based on meter list?
circuit_dict_list = og.get_circuit_dict_list(mains=False)
#meter_list = ['ml01', 'ml02', 'ml03', 'ml04', 'ml05', 'ml06', 'ml07', 'ml08']
meter_list = ['ug01', 'ug02', 'ug03', 'ug04', 'ug05', 'ug06', 'ug07', 'ug08']
# get daily energy for each circuit

import pandas as p
import numpy as np
all_energy = p.Series()
all_energy = np.array([])
num_circuits = 0
for cd in circuit_dict_list:
    #print 'querying'
    if cd['meter_name'] not in meter_list:
        continue
    num_circuits += 1
    print num_circuits
    de = og.get_daily_energy_for_circuit_id(cd['circuit_id'], date_start, date_end)
    if de == None:
        continue
    #de.values.astype(float)
    all_energy = np.hstack((all_energy, de.values))

    # append de.values to all_energy
#1/0

# remove zeros
remove_zeros = True
#remove_zeros = False
if remove_zeros:
    all_energy = all_energy[all_energy > 0]
# concatenate

# plot histogram
import matplotlib.pyplot as plt
f = plt.figure()
ax = f.add_axes((0.2,0.3,0.6,0.6))
import numpy as np
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

#ax.set_title('Mali Daily Electricity Consumption')
#ax.set_title('Uganda Mains Electricity Consumption')
#f.savefig(country+'_mains_histogram.pdf')
#f.savefig('mali_histogram.pdf')
f.savefig('uganda_histogram.pdf')

print 'number of datapoints = ', len(all_energy)
print 'possible observations = ', num_circuits * (date_end - date_start).days

