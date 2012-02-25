'''
energy_integrity.py
--------------------
from issue #18

for a given date range and circuit, output

number of expected observations
number of actual observation
ratio of actual to expected observations
number of days with correct midnight samples
number of days with corrupted midnight samples
ratio of corrupted midnight samples to total midnight samples

'''

# get list of pins corresponding to meters in meter_list
import offline_gateway as og
circuit_dict_list = og.get_circuit_dict_list()

# use subsample while debugging
#circuit_dict_list = circuit_dict_list[:1]
#circuit_dict_list = [{'circuit_id':294}]


# choose date range
import datetime as dt
date_start = dt.datetime(2012, 1, 1)
date_end   = dt.datetime(2012, 2, 1)

bd = {}
for i, c in enumerate(circuit_dict_list):

        # query database
        print 'querying for', i, 'th circuit =', c['circuit_id']
        watthours = og.get_watthours_for_circuit_id(c['circuit_id'], date_start, date_end)

        #1/0
        # watthours returns null if empty query
        if watthours == None:
            continue
        #if watthours == -1:
        #    continue

        print 'calculating'

        actual_observations = len(watthours)
        expected_observations = (date_end - date_start).days * 24

        #print "actual_observations", actual_observations
        #print "expected_observations", expected_observations
        #print "ratio", float(actual_observations) / expected_observations

        import pandas as p
        # create series with date-only index for 23 sample
        wh23 = watthours[[True if i.hour == 23 else False for i in watthours.index]]
        in23 = [dt.datetime(i.year, i.month, i.day) for i in wh23.index]
        wh23 = p.Series(data=wh23.values, index=in23)

        # create series with day-before date-only index for midnight sample
        wh24 = watthours[[True if i.hour == 0 else False for i in watthours.index]]
        in24 = [dt.datetime(i.year, i.month, i.day) - dt.timedelta(days=1) for i in wh24.index]
        wh24 = p.Series(data=wh24.values, index=in24)

        # combine wh23 and wh24 into data frame
        d = {'wh23':wh23, 'wh24':wh24}
        df = p.DataFrame(d)

        dfd = df['wh24'] - df['wh23']

        correct = len(dfd[dfd >= 0])
        corrupt = len(dfd[dfd < 0])
        #print "observations with both 11pm and midnight", dfd.count()
        #print "correct midnight behavior", correct
        #print "corrupted at midnight", corrupt
        #print "corrpution ratio", float(corrupt) / dfd.count()

        d = {}
        d['act_obs'] = actual_observations
        d['exp_obs'] = expected_observations
        d['rat_obs'] = float(actual_observations) / expected_observations
        d['mid_obs'] = dfd.count()
        d['ratio_correct'] = float(correct) / dfd.count()

        bd[c['meter_name'] + '-' + c['ip_address'][-2:]] = d


import pandas as p
bdf = p.DataFrame(bd)

bdf = bdf.T
bdf.to_csv('energy_integrity.csv')



# create histogram of corruption ratio
import matplotlib.pyplot as plt
plt.hist(bdf['ratio_correct'], cumulative=True, normed=True)
plt.xlabel('percent of correct reporting')
plt.grid(True)
plt.title('cumulative histogram of meter reset accuracy')
plt.savefig('energy_integrity.pdf')