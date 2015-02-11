#!/bin/bash -e

apt-get update

apt-get install -y wget
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - http://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

apt-get update
apt-get install -y postgresql-9.4

if [[ `sudo -u postgres psql -tAc "select 1 from pg_roles where rolname='loan_requests'"` != "1" ]]
then
    sudo -u postgres psql -qc "create role loan_requests login password 'loan_requests';"
fi

if [[ `sudo -u postgres psql -tAc "select 1 from pg_database where datname='loan_requests'"` != "1" ]]
then
    sudo -u postgres psql -qc "create database loan_requests with owner loan_requests;"
fi




