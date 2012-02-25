'''
credit_histogram_hourly.py
=========================

plot histogram of all hourly credit values for a list of meters in meter_name

y axis - frequency of observation

x axis - amount of credit in account

'''


figure_file_name = 'credit_histogram.pdf'
mains_ip = '192.168.1.200'
meter_names = ('ml01','ml02','ml03', 'ml04', 'ml05', 'ml06', 'ml07', 'ml08')

def credit_histogram(meter_names, date_start, date_end, axes):
    #def percentage_with_credit():
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    vpl = sa.Table('view_primary_log', metadata, autoload=True)

    # query all credit values from the database
    query = sa.select([vpl.c.credit],
                       whereclause=sa.and_(vpl.c.meter_timestamp>date_start,
                                           vpl.c.meter_timestamp<date_end,
                                           vpl.c.meter_name.in_(meter_names),
                                           vpl.c.ip_address!=mains_ip)
                      )
    #print query
    result = query.execute()

    credit = []
    for r in result:
        credit.append(r.credit)

    #print credit


    axes.hist(credit, bins=range(-100,3100,100), normed=True)
    axes.set_title(str(date_start) + ' to ' + str(date_end))


    #f.savefig(figure_file_name)

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    f, ax = plt.subplots(4, 1)

    import datetime as dt

    date_start = dt.datetime(2011, 9, 01)
    date_end   = dt.datetime(2011, 10, 01)
    credit_histogram_hourly(meter_names=meter_names,
                     date_end=date_end,
                     date_start=date_start,
                     axes=ax[0]
                     )

    date_start = dt.datetime(2011, 10, 01)
    date_end   = dt.datetime(2011, 11, 01)
    credit_histogram_hourly(meter_names=meter_names,
                     date_end=date_end,
                     date_start=date_start,
                     axes=ax[1]
                     )

    date_start = dt.datetime(2011, 11, 01)
    date_end   = dt.datetime(2011, 12, 01)
    credit_histogram_hourly(meter_names=meter_names,
                     date_end=date_end,
                     date_start=date_start,
                     axes=ax[2]
                     )

    date_start = dt.datetime(2011, 12, 01)
    date_end   = dt.datetime(2012,  1, 01)
    credit_histogram_hourly(meter_names=meter_names,
                     date_end=date_end,
                     date_start=date_start,
                     axes=ax[3]
                     )

    plt.show()