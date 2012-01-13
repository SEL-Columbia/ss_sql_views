'''
num meter reporting.py
======================
queries database for number of meters reporting over given time range
'''

# todo: update to sqlalchemy

def num_meters_reporting():
    import psycopg2
    conn = psycopg2.connect('dbname=gateway')
    cursor = conn.cursor()

    # note that if no meters are reporting, a zero is not reported
    # rather that date is not present

    query = '''
            select meter_timestamp, count(*)
            from view_primary_log
            where meter_timestamp > '2011-11-01' and
            meter_timestamp < '2011-12-31' and
            ip_address like '%200' and
            meter_name like 'ug%'
            group by meter_timestamp
            order by meter_timestamp;
            '''

    shniz = cursor.execute(query)
    shniz = cursor.fetchall()

    dates = []
    num_reporting = []

    for s in shniz:
        dates.append(s[0])
        num_reporting.append(s[1])

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_axes((0.1,0.1,0.8,0.8))

    ax.plot_date(dates,num_reporting, 'k-o')
    ax.set_title("Number of Mains Meters Reporting in Uganda")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Meters")
    ax.set_ylim((0,10))
    ax.grid()
    plt.show()

if __name__=='__main__':
    num_meters_reporting()