#!/bin/bash
# `trap` can be used to execute a certain function (in this case `exit`) when a given signal is received.
# This has the purpose of being able to stop the container from within (https://stackoverflow.com/questions/31538314/stopping-docker-container-from-inside). 
echo "I am running with pid $$"
echo $$ > /code/APPPID 
export VENV=$(poetry env info --path)
if [ $DJANGO_SETTINGS_MODULE = "mysite.settings.dev" ]  
then 
	echo "Development"
	# In development, the local repository should be mounted as a volume and changes are available that way.
	$VENV/bin/gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3 --reload  --error-logfile - --log-file - --log-level debug
else 
	echo "Production"
	# In production the repo does not need to be present on the host. The repo changes are pulled right into the container before the app starts.
	git pull --ff-only
	$VENV/bin/python manage.py migrate
	$VENV/bin/python manage.py collectstatic --noinput
	$VENV/bin/gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi
