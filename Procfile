release: python manage.py migrate
web: python manage.py runserver 0.0.0.0:$PORT
worker: celery -A blog worker -l INFO -P solo
worker: celery -A blog beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
