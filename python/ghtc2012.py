import offline_gateway as og
import datetime as dt
import matplotlib.pyplot as plt

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

if __name__ == '__main__':

    date_start = dt.datetime(2012, 2, 15)
    date_end = dt.datetime(2012, 4, 15)

    plot_two_ldc(date_start, date_end)