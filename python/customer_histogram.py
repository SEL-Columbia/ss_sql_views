# pulls all customer midnight samples and creates histogram
import sqlalchemy as sa

# create metadata object
metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

# define table objects from database
vm = sa.Table('view_midnight', metadata, autoload=True)

# query database
query = sa.select([vm.c.watthours, vm.c.name],
                   whereclause = sa.and_(vm.c.ip_address != '192.168.1.200',
                                       vm.c.watthours>0))
print query

# stuff array
result = query.execute()

watthour_list = []
for r in result:
    if 'ml' in r.name:
        watthour_list.append(r.watthours)

# graph histogram
import matplotlib.pyplot as plt

f, ax = plt.subplots(1,1)
import numpy as np
ax.hist(watthour_list, bins=np.linspace(0,200,41))
ax.set_xlabel('Daily Electrical Energy Consumed (Wh)')
ax.set_ylabel('Number of Days Observed')
ax.set_title('Mali Daily Electricity Consumption')
f.savefig('mali_histogram.pdf')

#plt.show()