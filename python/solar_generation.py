'''
solar_generation.py
===================
this script (will) fits a line to the solar kwh data to determine

the average daily kwh performance of the solar panel system
'''
def solar_generation():
    import sqlalchemy as sa

    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')

    # define table objects from database
    vs = sa.Table('view_solar', metadata, autoload=True)

    query = sa.select([vs.c.meter_name], distinct=True, order_by=vs.c.meter_name)
    print query

    # get list of meter names in solar logs
    meter_list = []
    result = query.execute()
    for r in result:
        meter_list.append(r.meter_name)



    for meter_name in meter_list:
        # get data in date range
        # fit linear
        # report slope, show graph

        query = sa.select([sa.func.max(vs.c.meter_timestamp),
                           sa.func.min(vs.c.meter_timestamp),
                           sa.func.max(vs.c.solar_kwh),
                           sa.func.min(vs.c.solar_kwh)],
                            whereclause=vs.c.meter_name == meter_name)
        result = query.execute().fetchone()
        #print result.keys()
        days_elapsed = (result.max_1-result.min_1).days
        watt_hours = result.max_2-result.min_2
        print meter_name, days_elapsed, watt_hours, watt_hours/days_elapsed

if __name__ == '__main__':
    solar_generation()