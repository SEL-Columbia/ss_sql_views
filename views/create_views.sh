psql -d gateway -f create_view_primary_log.sql 
psql -d gateway -f create_view_midnight.sql 
psql -d gateway -f create_view_meter.sql
