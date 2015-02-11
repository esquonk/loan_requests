#!/bin/bash -e

SITE_ROOT="/srv/loan_requests"

easy_install pip
pip install --upgrade virtualenv

virtualenv /srv/loan_requests/env

ln -sf $SITE_ROOT/project/deploy/nginx_site.conf /etc/nginx/sites-enabled/loan_requests
cp -f $SITE_ROOT/project/deploy/uwsgi_upstart.conf /etc/init/uwsgi_loan_requests.conf

$SITE_ROOT/env/bin/pip install uwsgi
$SITE_ROOT/env/bin/pip install --pre --no-index --find-links file://$SITE_ROOT/project/deploy/python_packages -r $SITE_ROOT/project/deploy/requirements.txt
$SITE_ROOT/env/bin/python $SITE_ROOT/project/manage.py collectstatic --noinput
$SITE_ROOT/env/bin/python $SITE_ROOT/project/manage.py migrate

service nginx reload

if ( initctl status uwsgi_loan_requests | grep start ); then
  initctl stop uwsgi_loan_requests
fi
start uwsgi_loan_requests