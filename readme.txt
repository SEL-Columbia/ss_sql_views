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

> PATH="/Library/PostgreSQL/9.0/bin:${PATH}"
> export PATH

set connection to trust in pg_hba.conf
> sudo emacs /Library/PostgreSQL/9.0/data/pg_hba.conf


helpful commands
----------------
> pg_dump gateway >> dumpfile.sql


creates database named database_to_create
> createdb database_to_create

deletes database from postgres
> dropdb database_to_delete

load data into gateway database
> psql -f dumpfile.sql -d gateway


to run script in psql
\i script.sql

\d and \d+ for schema


matt notes:
-----------
change 8192 to 393216 in last line of /etc/sysctl.conf

