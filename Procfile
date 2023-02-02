release: python manage.py migrate
web: python manage.py runserver 0.0.0.0:$PORT
worker: celery worker --app=blog.app
