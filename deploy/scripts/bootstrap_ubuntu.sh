#!/bin/bash -e

SITE_ROOT=/srv/loan_requests

mkdir -p $SITE_ROOT/static
mkdir -p $SITE_ROOT/log
mkdir -p $SITE_ROOT/log/uwsgi
mkdir -p $SITE_ROOT/log/nginx

apt-get update
apt-get install -y nginx python python-setuptools
apt-get install -y build-essential python-all-dev libpq-dev

rm -f /etc/nginx/sites-enabled/default

/bin/bash -e $SITE_ROOT/project/deploy/scripts/dbserver_install.sh
/bin/bash -e $SITE_ROOT/project/deploy/scripts/project_install.sh
/bin/bash -e $SITE_ROOT/project/deploy/scripts/load_test_data.sh
