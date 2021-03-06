#!/bin/bash
# Start cron 
cron
# Start wagtail
export VENV=$(poetry env info --path)
if [ "$DJANGO_SETTINGS_MODULE" = "mysite.settings.dev" ]  
then 
	echo "Detected development environment."
	# In development, the local repository should be mounted as a volume and changes are available that way.
	$VENV/bin/python manage.py runserver 0:8000
else 
	echo "Detected production environment."
	$VENV/bin/python manage.py migrate
	$VENV/bin/python manage.py collectstatic --noinput
	$VENV/bin/gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi
