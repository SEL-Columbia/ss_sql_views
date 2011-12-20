this repo has sql views and queries for analyzing sharedsolar data using
postgresql features

Daniel Soto
Modi Lab, Columbia University
20 dec 2011



os x installation notes

download PostgreSQL
http://www.enterprisedb.com/products-services-training/pgdownload#osx

add to .bash_profile:
> export PGUSER postgres

set connection to TRUST in pg_hba.conf
> sudo emacs /Library/PostgreSQL/9.0/data/pg_hba.conf


helpful commands
----------------
pg_dump gateway >> dumpfile.sql

createdb database_to_create

dropdb database_to_delete

load data into gateway database
> psql -f dumpfile.sql -d gateway


to run script in psql
\i script.sql