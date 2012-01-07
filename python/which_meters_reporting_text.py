# this script provides a text output of reporting meters per hour
# 'reporting' is defined as if the 'mains' reports

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

date_start = datetime.datetime(2011,12,1)
date_end = datetime.datetime(2012, 1, 1)

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
