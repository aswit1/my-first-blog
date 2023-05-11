### Summary of project:
This project is a blog site that does require a login to view most features. It contains a main blog, where 
only the admin can post, and a community blog, where anybody who is logged in can post. Both blogs allow for 
comments, which can be edited and deleted by the owner, and the owner can also edit and delete their blog posts
as well. The admin has the ability to delete any posts or comments. This site also includes a polls section,
where anybody can post a poll with as many options as they choose; anyone who is logged in can vote on any polls.
Also included in this blog site is the ability to send direct messages to an individual user or a group; when 
users recieve new direct messages, their chat with that person will show up as new and the navigation bar changes
colors for the messages link. Finally, any user has the ability to view and edit their profile, and the admin can 
view and edit any users' profiles as well as click on links to the admin site and links that test some features of
the site. These features include the weather and email tests. The site displays the weather so an admin can use
the test link if the weather is not updating correctly, and the email test link sends an email to the users that
have allowed it in their profile if there are any new posts, which should be sending automatically if everything
is working properly.
###
### How to set up the project from Github:
- Start by creating a new folder
- Open a Command Prompt and use cd (name of folder)
- Copy the link from the Github  clone page and type: git clone (link)
- Use, cd (my-first-blog), to get into the blog in the folder
- Type, python -m venv myenv, to set up your virtual environment
- Then, to activate your virtual environment type: \myenv\Scripts\activate
  - Make sure it says (myenv) in the next line on the command prompt
- Type: pip install -r requirements.txt
- Then, to temporarily set an environmental variable for your CURRENT command prompt session:
  - Type: set SECRET_KEY=hellothere
  - This will expire when you close the command prompt
- Type: python manage.py migrate
- Then: python manage.py runserver
- Finally, you can copy the link pasted by the runserver command into your browser, which will open the main site.

### 
#### You need several environmental variables set to run this code.
### They are:
- EMAIL_HOST_PASSWORD
- DEFAULT_FROM_EMAIL
- and WEATHER_API_KEY

#### Celery also needs to be set up to run specific tasks in this project...

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
