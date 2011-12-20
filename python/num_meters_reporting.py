import psycopg2
conn = psycopg2.connect('dbname=gateway')
cursor = conn.cursor()

query = '''
        select date, count(*)
        from primary_log_view
        where date>'2011-11-01' and
        date<'2011-12-31' and
        ip_address like '%200' and
        name like 'ug%'
        group by date
        order by date;
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

ax.plot_date(dates,num_reporting, 'kx')
ax.set_title("Number of Mains Meters Reporting in Uganda")
ax.set_xlabel("Date")
ax.set_ylabel("Number of Meters")
ax.set_ylim((0,10))
ax.grid()
plt.show()

