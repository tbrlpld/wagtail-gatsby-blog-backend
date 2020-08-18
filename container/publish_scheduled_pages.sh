#!/bin/bash
scriptdir=$(realpath $(dirname $0))
basedir=$(realpath $(dirname $scriptdir))
cd $basedir
# Ensure environment variables are available. Cron is run by the system with a
# minimal environment. This means that the variables that you expect from the 
# normal shell to be available, are not. 
source $basedir/.env
venv=$(/usr/local/bin/poetry env info --path)
echo "
$(date +%Y-%m-%d\ %H:%M:%S) Publishing pages"
$venv/bin/python $basedir/manage.py publish_scheduled_pages
