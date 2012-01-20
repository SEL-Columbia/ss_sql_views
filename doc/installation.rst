Installation
============

These notes are written mainly for OS X users, but Linux users should be
able to follow along with little trouble.

We are going to install

- Pip - a library that allows for downloading of python libraries
- PostgreSQL - a database
- psycopg2 - a library that allows python to talk to postgresql
- SQLalchemy - a library that allows python to talk to databases
- ss_sql_views - this library for queries of gateway usage data

Optionally we can install

- sphinx - library that allows generation of documentation

Pip
---

Assuming you have easy_install from your python installation, you can install pip using::

    easy_install pip

PostgreSQL
----------

download PostgreSQL from::

    http://www.enterprisedb.com/products-services-training/pgdownload#osx

add to .bash_profile::

    > export PGUSER postgres
    > PATH="/Library/PostgreSQL/9.0/bin:${PATH}"
    > export PATH

set connection to trust in pg_hba.conf::

    > sudo emacs /Library/PostgreSQL/9.0/data/pg_hba.conf

psycopg2
--------

install psycopg2 (on os x, i had to install this from source) download then,::

    > sudo python setup.py install

probably better to use pip::

    > pip install psycopg2

sqlalchemy
----------

install sqlalchemy (need 0.7 or higher, use --upgrade if necessary)::

    > pip install sqlalchemy

ss_sql_views
------------

download repo from github::

    git clone git@github.com:modilabs/ss_sql_views.git


sphinx
-------------

install sphinx to create docs locally::

    > easy_install sphinx

to generate docs, navigate to doc/ directory and run::

    > make html
    > make latexpdf


versions needed
---------------
On my development machine OSX 10.6.8, I have

- python 2.7.2
- sqlalchemy 0.7.4

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

