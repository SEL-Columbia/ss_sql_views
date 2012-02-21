'''
shared library for offline gateway
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
                   whereclause=sa.and_(t.c.meter_name.in_(meter_list),
                                       t.c.ip_address!='192.168.1.200'))
    result = q.execute()

    pl = [r.pin for r in result]
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

'''
takes circuit_id and returns pandas series for watthours
between date_start and date_end

warning - does not gracefully handle empty query result
'''
def get_watthours_for_circuit_id(circuit_id, date_start, date_end):
    import sqlalchemy as sa
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')
    t = sa.Table('view_primary_log', metadata, autoload=True)
    query = sa.select([sa.func.max(t.c.watthours).label('watthours'),
                       t.c.meter_timestamp],
                       whereclause=sa.and_(t.c.circuit_id==circuit_id,
                                           t.c.meter_timestamp<date_end,
                                           t.c.meter_timestamp>date_start),
                       order_by=t.c.meter_timestamp,
                       group_by=t.c.meter_timestamp,
                       distinct=True)
    result = query.execute()
    # todo: deal with empty query result
    import pandas as p
    gd = p.DataFrame(result.fetchall(), columns=result.keys())
    gd = p.Series(gd['watthours'], index=gd['meter_timestamp'])
    return gd

'''
gets circuit list for all circuits in database
'''
def get_circuit_list():
    import sqlalchemy as sa
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')
    vm = sa.Table('view_meter', metadata, autoload=True )
    # get list of circuits
    query = sa.select([vm.c.circuit_id,
                       vm.c.meter_name,
                       vm.c.ip_address],
                       order_by=(vm.c.meter_name, vm.c.ip_address)
                       )
    result = query.execute()
    circuit_list = []
    for r in result:
        circuit_list.append((r.circuit_id, r.meter_name, r.ip_address))
    return circuit_list