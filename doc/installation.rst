Installation
============

download repo from github::

    git clone git@github.com:modilabs/ss_sql_views.git

os x installation notes

download PostgreSQL from::

    http://www.enterprisedb.com/products-services-training/pgdownload#osx

add to .bash_profile::

    > export PGUSER postgres
    > PATH="/Library/PostgreSQL/9.0/bin:${PATH}"
    > export PATH

set connection to trust in pg_hba.conf::

    > sudo emacs /Library/PostgreSQL/9.0/data/pg_hba.conf


install sqlalchemy::

    > easy_install sqlalchemy

to dump gateway to a file::

    > pg_dump gateway >> dumpfile.sql


creates database named database_to_create::

    > createdb database_to_create

deletes database from postgres::

    > dropdb database_to_delete

load data into gateway database::

    > psql -f dumpfile.sql -d gateway


to run script in psql::

    \i script.sql

\d and \d+ for schema
