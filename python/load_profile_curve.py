



if __name__ == '__main__':

    import sqlalchemy as sa
    import matplotlib.pyplot as plt
    import datetime as dt

    date_start = dt.datetime(2011, 10, 1)
    date_end = dt.datetime(2012, 3, 1)

    import offline_gateway as og
    circuit_list = og.get_circuit_list()

    debug = False
    debug = True
    if debug:
        circuit_list = circuit_list[:1]

    # iterate over list of circuits
    for c in circuit_list:
        filename = 'lpc-' + c[1] + '-' + c[2][-3:] + '.pdf'
        print 'querying for', filename

        import offline_gateway as og
        df, error = og.get_watthours_for_circuit_id(c[0], date_start, date_end)

        if error != 0:
            continue
        # calculate discrete derivative
        import pandas as p
        offset = df - df.shift(1, offset=p.DateOffset(hours=1))

        positive_only = True
        #positive_only = False
        if positive_only:
            offset = offset[offset.values >= 0]

        # order values
        #1/0
        offset.sort()

        #1/0

        # plot each circuit daily energy values for all time
        f, ax = plt.subplots(1, 1, sharex=True)

        ax.plot(offset.values, mfc='#dddddd')
        #ax.set_xlabel('Date')
        ax.set_ylabel('Average Hourly Power')
        #ax.set_xlim((date_start, date_end))
        ax.set_title(filename)
        #f.autofmt_xdate()
        f.savefig(filename)
        plt.close()