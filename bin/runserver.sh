export VENV=$(poetry env info --path)
if [ $DJANGO_SETTINGS_MODULE = "mysite.settings.dev" ]  
then 
	echo "Development"
	$VENV/bin/gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3 --reload  --error-logfile - --log-file - --log-level debug
else 
	echo "Production"
	$VENV/bin/python manage.py migrate
	$VENV/bin/python manage.py collectstatic --noinput
	$VENV/bin/gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi
