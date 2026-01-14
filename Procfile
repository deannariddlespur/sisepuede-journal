release: python manage.py migrate && python manage.py create_superuser
web: gunicorn journal.wsgi:application --bind 0.0.0.0:$PORT

