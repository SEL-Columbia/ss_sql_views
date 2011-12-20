import psycopg2
conn = psycopg2.connect('dbname=gateway')
cursor = conn.cursor()

meter_name = 'ug04'
date_start = '20111001'
date_end = '20111201'

query = """select *
           from midnight_rider
           where name = '%s' and
                 ip_address = '192.168.1.200' and
                 date >= '%s' and
                 date <= '%s'
           order by date
        """ % (meter_name, date_start, date_end)

shniz = cursor.execute(query)
shniz = cursor.fetchall()

dates = []
watthours = []

for s in shniz:
    dates.append(s[0])
    watthours.append(s[2])

import pylab
pylab.plot_date(dates,watthours)
pylab.grid()
pylab.show()

