export VENV=$(poetry env info --path)
$VENV/bin/python manage.py migrate
$VENV/bin/python manage.py collectstatic --noinput
$VENV/bin/gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3 --error-logfile - --log-file - --log-level debug