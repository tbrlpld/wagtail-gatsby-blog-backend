#!/bin/bash

# Switch to shell of user dockrunner (if not already active)
if [ "$USER" != "dockrunner" ]
then
	sudo -u dockrunner bash
	userswitch=1 
else
	userswitch=0
fi

scriptdir=$(realpath $(dirname $0))
basedir=$(realpath $(dirname $scriptdir))

docker-compose -f $basedir/docker-compose.yml pull
docker-compose -f $basedir/docker-compose.yml up --no-start
docker cp $basedir/data wagtail-gatsby-blog-wagtail:/code

# Leave shell of user dockrunner if switched to automatically
if [ $userswitch = 1 ]; 
then 
	exit
fi