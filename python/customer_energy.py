# 12/20/11 10:31 PM
# fixme: needs to use view_primary_log

import psycopg2
conn = psycopg2.connect('dbname=gateway')
cursor = conn.cursor()

meter_name = 'ml03'
date_start = '20111015'
date_end = '20111201'

columns = ('sum(watthours)',
           'meter_timestamp')

query = """
        select %s, %s
        from view_primary_log
        where meter_name = '%s' and
              meter_timestamp > '%s' and
              meter_timestamp < '%s' and
              ip_address!='192.168.1.200'
              group by meter_timestamp
              order by meter_timestamp;
        """ % (columns[0], columns[1], meter_name, date_start, date_end)

cursor.execute(query)
shniz = cursor.fetchall()

dates = []
watthours = []

for s in shniz:
    dates.append(s[1])
    watthours.append(s[0])

import pylab
pylab.plot_date(dates,watthours,'ko-')
pylab.grid()
pylab.show()

