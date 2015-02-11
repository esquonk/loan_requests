#!/bin/bash

SITE_ROOT="/srv/loan_requests"

$SITE_ROOT/env/bin/python $SITE_ROOT/project/manage.py loaddata $SITE_ROOT/project/test_data/dump.json