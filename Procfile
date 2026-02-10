release: python manage.py migrate --noinput && python manage.py create_superuser || true
web: python manage.py collectstatic --noinput && gunicorn journal.wsgi:application --bind 0.0.0.0:$PORT

