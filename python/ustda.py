import offline_gateway as og

og.plot_customer_energy_histogram(meter_list=['ml01', 'ml02', 'ml03', 'ml04', 'ml05', 'ml06', 'ml07', 'ml08'],
                                   title='Mali Customer Daily Energy Histogram',
                                   filename='ustda_Mali_Histogram.pdf')
og.plot_customer_energy_histogram(meter_list=['ug01', 'ug02', 'ug03', 'ug04', 'ug05', 'ug06', 'ug07', 'ug08'],
                                   title='Uganda Customer Daily Energy Histogram',
                                   filename='ustda_Uganda_Histogram.pdf')
