import psycopg2
conn = psycopg2.connect('dbname=gateway')
cursor = conn.cursor()

meter_name = 'ml03'
date_start = '20111015'
date_end = '20111201'

columns = ('sum(watthours)',
           'date')

query = """
        select %s, %s
        from primary_log_view
        where name = '%s' and
              date > '%s' and
              date < '%s' and
              ip_address!='192.168.1.200'
              group by date
              order by date;
        """ % (columns[0], columns[1], meter_name, date_start, date_end)

shniz = cursor.execute(query)
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

