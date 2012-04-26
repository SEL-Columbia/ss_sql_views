
# todo: convert to use circuit_dict_list


if __name__ == '__main__':

    import sqlalchemy as sa
    import matplotlib.pyplot as plt
    import datetime as dt

    date_start = dt.datetime(2012, 3, 1)
    date_end = dt.datetime(2012, 4, 1)

    import offline_gateway as og
    circuit_list = og.get_circuit_list()

    debug = True
    debug = False
    if debug:
        circuit_list = circuit_list[:1]

    # iterate over list of circuits
    for c in circuit_list:
        filename = 'lpc-' + c[1] + '-' + c[2][-3:] + '.pdf'
        print 'querying for', filename

        og.plot_load_profile_curve(c[0], date_start, date_end, filename)