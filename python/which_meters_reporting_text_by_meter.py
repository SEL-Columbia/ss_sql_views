'''
which_meters_reporting_text.py
==============================

this script provides a text output of reporting meters per hour
'reporting' is defined as if the 'mains' reports
'''

def which_meters_reporting_text():
    import psycopg2
    conn = psycopg2.connect('dbname=gateway')
    cursor = conn.cursor()


    # get this list from meter database query
    clist=['ml00','ml01','ml02','ml03','ml04',
           'ml05','ml06','ml07','ml08',
           'ug01','ug02','ug03','ug04',
           'ug05','ug06','ug07','ug08']
    import datetime
    this_date = datetime.datetime(2011,12,1,0,0)

    date_start = datetime.datetime(2011,12,31)
    date_end = datetime.datetime(2012, 3, 4)

    start = date_start
    while 1:
        # set endpoint at end of hour
        this_date = start + datetime.timedelta(hours=1)

        query = '''
            select meter_name
            from view_primary_log
            where meter_timestamp = '%s' and
            ip_address = '192.168.1.200'
            order by meter_name;
            ''' % this_date

        shniz = cursor.execute(query)
        shniz = cursor.fetchall()

        meter_list = [s[0] for s in shniz]

        # output to screen starting with date and then circuit_id or hyphen
        print start,
        print "".join([str(x).ljust(5) if x in meter_list else ' --- ' for x in clist])
        # increment date and check for end condition
        start = start + datetime.timedelta(hours=1)
        if start >= date_end:
            break

if __name__ == '__main__':
    meter_name = 'ml08'
    import sqlalchemy as sa
    # create metadata object
    metadata = sa.MetaData('postgres://postgres:postgres@localhost:5432/gateway')
    # define table objects from database
    t = sa.Table('view_primary_log', metadata, autoload=True)

    # set date ranges
    import datetime as dt
    now        = dt.datetime.now()
    date_end   = dt.datetime(now.year, now.month, now.day)
    date_start = date_end - dt.timedelta(days=5)

    this_date = date_start
    while 1:
        query = sa.select([t.c.ip_address],
                      whereclause=sa.and_(t.c.meter_timestamp == this_date,
                                          t.c.meter_name == meter_name),
                       order_by=t.c.meter_name)
        result = query.execute()
        circuits = result.fetchall()
        #1/0
        clist = [elem[0][-3:] for elem in circuits]
        clist.sort()
        clist = [int(c) for c in clist]
        possible_circuits = range(200,222)
        print this_date,
        for pc in possible_circuits:
            if pc in clist:
                print pc,
            else:
                print '---',
        print

        this_date = this_date + dt.timedelta(hours=1)
        if this_date >= date_end:
            break
