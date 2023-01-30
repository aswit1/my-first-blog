You need three environmental variables set to run this code.
### They are:
- EMAIL_HOST_PASSWORD
- DEFAULT_FROM_EMAIL
- and WEATHER_API_KEY

# Deployment Steps:
### On development machine:
- pip freeze >> requirements.txt (only if you've newly installed packages)
- git add -A (add all files to git)
- git commit -m "your message" (create a commit for github)
- git push
### On production machine:
- git pull
- pip install -r requirements.txt
- python manage.py migrate 
- reload
