import offline_gateway as og
import datetime as dt
import matplotlib.pyplot as plt

def plot_two_ldc(date_start, date_end):
    f, ax = plt.subplots(1, 1)
    og.plot_load_profile_curve_to_axis(57, date_start, date_end, ax, label='Lighting')
    og.plot_load_profile_curve_to_axis(123, date_start, date_end, ax, label='Lighting and Freezer')
    ax.legend()
    ax.set_xlabel('Fraction of Availability')
    ax.grid(True, linestyle='-', color='#cccccc')
    ax.set_title('Load Demand Curve for Microgrids')
    plt.savefig('ustda_load_demand_curve.pdf')

if __name__ == '__main__':

    date_start = dt.datetime(2012, 2, 15)
    date_end = dt.datetime(2012, 4, 15)
    plot_two_ldc(date_start, date_end)

    '''
    og.plot_customer_energy_histogram(meter_list=['ml01', 'ml02', 'ml03', 'ml04', 'ml05', 'ml06', 'ml07', 'ml08'],
                                       title='Mali Customer Daily Energy Histogram',
                                       filename='ustda_Mali_Histogram.pdf')
    og.plot_customer_energy_histogram(meter_list=['ug01', 'ug02', 'ug03', 'ug04', 'ug05', 'ug06', 'ug07', 'ug08'],
                                       title='Uganda Customer Daily Energy Histogram',
                                       filename='ustda_Uganda_Histogram.pdf')
    '''
