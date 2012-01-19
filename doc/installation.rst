Installation
============

download repo from github::

    git clone git@github.com:modilabs/ss_sql_views.git

os x installation notes
-----------------------

download PostgreSQL from::

    http://www.enterprisedb.com/products-services-training/pgdownload#osx

add to .bash_profile::

    > export PGUSER postgres
    > PATH="/Library/PostgreSQL/9.0/bin:${PATH}"
    > export PATH

set connection to trust in pg_hba.conf::

    > sudo emacs /Library/PostgreSQL/9.0/data/pg_hba.conf

install psycopg2 (on os x, i had to install this from source) download then,::

    > sudo python setup.py install

install sqlalchemy::

    > easy_install sqlalchemy

documentation
-------------

install sphinx to create docs locally::

    > easy_install sphinx

to generate docs, navigate to doc/ directory and run::

    > make html
    > make latexpdf


versions needed
---------------
On my development machine OSX 10.6.8, I have
python 2.7.2 and
sqlalchemy 0.7.4

get fresh copy of database
--------------------------

get data from database::

    # pull latest backup from gateway
    scp sharedsolar@gateway.sharedsolar.org:/var/lib/postgresql/backups/gateway.YYMMDD.sql.zip .
    unzip gateway.YYMMDD.sql.zip

    # delete current local backup of gateway
    dropdb gateway

    # recreate gateway database
    createdb gateway

    # load the sql dump into the gateway
    psql -d gateway -f var/lib/postgresql/backups/gateway.YYMMDD.sql


create views in database
------------------------

navigate to folder with views::

    cd ss_sql_views/views/

start postgres::

    > psql gateway

run script to create view in database::

    \i create_view_myview.sql

to verify that view has been created by listing all tables::

    \d

to inspect view columns and query in postgresql::

    \d+ view_myview

to exit psql::

    \q

