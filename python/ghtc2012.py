import offline_gateway as og
import datetime as dt
import matplotlib.pyplot as plt
import pandas as p

'''
 25 "ml00"
164 "ml01"
143 "ml02"
213 "ml03"
192 "ml04"
 57 "ml05"
 70 "ml06"
102 "ml07"
123 "ml08"
'''

# todo: fit solar generation over same time period

'''
print
print 'ml03'
og.analyze_load_profile_curve(213, date_start, date_end)
og.plot_load_profile_curve_to_file(213, date_start, date_end, 'ml03-ldc.pdf')


print
print 'ml05'
og.analyze_load_profile_curve(57, date_start, date_end)
og.plot_load_profile_curve_to_file(57, date_start, date_end, 'ml05-ldc.pdf')

print
print 'ml06'
og.analyze_load_profile_curve(70, date_start, date_end)
og.plot_load_profile_curve_to_file(70, date_start, date_end, 'ml06-ldc.pdf')

print
print 'ml07'
og.analyze_load_profile_curve(102, date_start, date_end)
og.plot_load_profile_curve_to_file(102, date_start, date_end, 'ml07-ldc.pdf')

print
print 'ml08'
og.analyze_load_profile_curve(123, date_start, date_end)
og.plot_load_profile_curve_to_file(123, date_start, date_end, 'ml08-ldc.pdf')
'''


def plot_two_ldc(date_start, date_end):
    f, ax = plt.subplots(1, 1)
    og.plot_load_profile_curve_to_axis(57, date_start, date_end, ax, label='Lighting')
    og.plot_load_profile_curve_to_axis(123, date_start, date_end, ax, label='Lighting and Freezer')
    ax.legend()
    ax.set_xlabel('Fraction of Availability')
    ax.grid(True, linestyle='-', color='#cccccc')
    plt.savefig('two_ldc.pdf')

def plot_two_bulb_profile(date_start, date_end):
    og.plot_hourly_power_profile(230, date_start, date_end, 'two_bulb_profile.pdf', title=False)

def plot_freezer_profile(date_start, date_end):
    og.plot_hourly_power_profile(96, date_start, date_end, 'freezer_profile.pdf', title=False)

def tbl_efficiency(date_start, date_end):
    print '% tbl_efficiency'
    print '%', date_start
    print '%', date_end
    dl = []
    for meter, cid in [('ml05', 57), ('ml06', 70), ('ml07', 102), ('ml08', 123)]:
        d = og.analyze_load_profile_curve(cid, date_start, date_end)
        og.plot_load_profile_curve_to_file(cid, date_start, date_end, meter+'-ldc.pdf')
        dl.append(d)
    df = p.DataFrame(dl)

    for row in df.index:
        print '%.2f' % df.ix[row]['capacity_factor'],
        print '&',
        print df.ix[row]['circuit_id'],
        print '\\\\'

if __name__ == '__main__':

    date_start = dt.datetime(2012, 2, 15)
    date_end = dt.datetime(2012, 4, 15)
    #plot_two_ldc(date_start, date_end)

    date_start = dt.datetime(2012, 1, 1)
    date_end = dt.datetime(2012, 3, 1)
    #plot_two_bulb_profile(date_start, date_end)

    #plot_freezer_profile(dt.datetime(2012, 2, 1), dt.datetime(2012, 4, 15))

    date_start = dt.datetime(2012, 2, 15)
    date_end = dt.datetime(2012, 4, 15)
    tbl_efficiency(date_start, date_end)