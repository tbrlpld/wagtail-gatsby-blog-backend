#!/bin/bash
scriptdir=$(realpath $(dirname $0))
basedir=$(realpath $(dirname $scriptdir))
cd $basedir
venv=$(/usr/local/bin/poetry env info --path)
echo "
$(date +%Y-%m-%d\ %H:%M:%S) Publishing pages"
$venv/bin/python $basedir/manage.py publish_scheduled_pages