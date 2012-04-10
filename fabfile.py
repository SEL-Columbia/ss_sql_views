'''
fabfile for offline gateway tasks
'''

import datetime as dt
from fabric.api import local, lcd, run, env

env.hosts = ['gateway.sharedsolar.org']
env.user = 'root'

def sync_db():
    time = dt.datetime.now().strftime('%y%m%d')
    file = 'gateway.' + time + '.sql.zip'
    url = 'root@gateway.sharedsolar.org'
    path = 'var/lib/postgresql/backups/'

    local('mkdir temp')
    with lcd('temp'):
        download_db(url, path, file)
        load_db(path, file)
    create_views()
    local('rm -rf temp')
    show_disk_space()


def download_db(url, path, file):
    # create local temp folder
    print 'Creating temporary folder ./temp'
    # create timestamp
    # create string for getting database

    # scp database
    print 'Downloading database from gateway'
    local('scp ' + url + ':/' + path + file + ' .')

    # locally unzip database
    print 'Expanding database'
    local('unzip ' + file)


def load_db(path, file):
    # if database exists, dropdb
    local('dropdb gateway')
    # create db
    local('createdb gateway')
    # load database
    print 'Loading database'
    local('psql -d gateway -f ' + path + file[:-4])


def create_views():
    print 'Executing create_views'
    # execute all sql files
    local('psql -d gateway -f views/create_view_primary_log.sql')
    local('psql -d gateway -f views/create_view_midnight.sql')
    local('psql -d gateway -f views/create_view_meter.sql')
    local('psql -d gateway -f views/create_view_alarms.sql')
    local('psql -d gateway -f views/create_view_solar.sql')
    local('psql -d gateway -f views/create_view_recharge.sql')

def show_disk_space():
    run('df -h')