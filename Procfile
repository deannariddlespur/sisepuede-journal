release: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py create_superuser || true
web: gunicorn journal.wsgi:application --bind 0.0.0.0:$PORT

