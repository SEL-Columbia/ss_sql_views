'''
script to create CSV of credit values for all circuits
will output CSV with
rows - individual circuits, identified by pin number
cols - credit sample for each date
'''

'''
returns list of pins for circuits in meter_list
'''
def get_pins(meter_list):
    import sqlalchemy as sa
    import pandas as p
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')
    t = sa.Table('view_meter', metadata, autoload=True)
    q = sa.select([t.c.pin],
                   whereclause=sa.and_(t.c.meter_name.in_(meter_list)))
    result = q.execute()

    pl = []
    for r in result:
        pl.append(r.pin)

    return pl


'''
takes pin and dates as input
returns pandas series of credit with dates as index
'''
def get_credit_for_pin(pin, date_start, date_end):
    import sqlalchemy as sa
    import pandas as p

    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')
    t = sa.Table('view_midnight', metadata, autoload=True)

    q = sa.select([t.c.meter_timestamp,
                   t.c.credit],
                   whereclause=sa.and_(t.c.meter_timestamp >= date_start,
                                       t.c.meter_timestamp < date_end,
                                       t.c.pin == pin),
                   order_by=t.c.meter_timestamp,
                   distinct=True)
    result = q.execute()

    gd = p.DataFrame(result.fetchall(), columns=result.keys())
    gd = p.Series(gd['credit'], index=gd['meter_timestamp'])

    return gd
    #return series

import offline_gateway as og

meter_list = ('ml01','ml02','ml03','ml04','ml07','ml08')
pins = og.get_pins(meter_list)

#1/0

import datetime as dt
date_start = dt.datetime(2011,9,1)
date_end = dt.datetime(2012,2,1)

d = {}
for i, pin in enumerate(pins):
    print 'querying for', i, 'th pin =', pin
    credit = og.get_credit_for_pin(pin, date_start, date_end)
    d[pin] = credit

import pandas as p
df = p.DataFrame(d)

print df

print df.T

df.T.to_csv('credit.csv')

    # append to larger data frame

# write out data frame to csv