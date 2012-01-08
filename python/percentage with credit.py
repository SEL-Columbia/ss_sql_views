from __future__ import division
import sqlalchemy

conn_string = 'postgres://postgres:postgres@localhost:5432/gateway'
engine = sqlalchemy.create_engine(conn_string)

metadata = sqlalchemy.MetaData()
metadata.bind = engine

# gets all the table info for free
view_primary_log = sqlalchemy.Table('view_primary_log', metadata, autoload=True)


query = view_primary_log.select(view_primary_log.c.credit == 500).execute()
query = view_primary_log.count(view_primary_log.c.credit <= 0).execute()


for q in query:
    zero = q[0]
    #print q['credit'], q['meter_timestamp'].isoformat()

query = view_primary_log.count(view_primary_log.c.credit > 0).execute()
for q in query:
    nonzero = q[0]

print 'samples with zero =', zero
print 'samples with nonzero =', nonzero
print 'percentage time with credit =', nonzero / (nonzero + zero)