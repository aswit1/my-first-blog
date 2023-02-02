release: python manage.py migrate
web: gunicorn mysite.wsgi
worker: celery -A blog worker -l INFO -B --scheduler django_celery_beat.schedulers:DatabaseScheduler -P solo
