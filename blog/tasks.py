from django.contrib.auth.models import User
from user_manager.models import UserProfile
from user_manager.views import all_users
from .models import Post
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from celery import shared_task

# def new_post_email():
#     new_posts = Post.objects.filter(new_post=True)
#     this_message = "<ul>"
#     for new_post in new_posts:
#         this_message += f'<li><a href="http://localhost:8000/post/{new_post.pk}">{new_post.title}</a></li>'
#     this_message += "</ul>"
#     message = Mail(
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to_emails='switaj.alexandria@olsohio.org',
#         subject='New Posts',
#         html_content=this_message
#     )
#     try:
#         sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
#         response = sg.send(message)
#         code, body, headers = response.status_code, response.body, response.headers
#         print(f"Response Code: {code} ")
#         print(f"Response Body: {body} ")
#         print(f"Response Headers: {headers} ")
#         print("Message Sent!")
#         # return str(response.status_code)
#         for post in new_posts:
#             post.new_post=False
#             post.save()
#     except Exception as e:
#         print("Error: {0}".format(e))
@shared_task
def update_emails():
    email_user_list = []
    new_posts = Post.objects.filter(new_post=True)
    if len(new_posts) < 1:
        return "no new posts"
    users = UserProfile.objects.all()
    for user in users:
        if user.email_updates is True:
            email_user_list.append(user.user.email)
    for each_user in email_user_list:
        new_post_email(each_user)


def new_post_email(email_address):
    new_posts = Post.objects.filter(new_post=True)
    this_message = "<ul>"
    for new_post in new_posts:
        this_message += f'<li><a href="http://localhost:8000/post/{new_post.pk}">{new_post.title}</a></li>'
    this_message += "</ul>"
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email_address,
        subject='New Posts',
        html_content=this_message
    )
    try:
        sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response Code: {code} ")
        print(f"Response Body: {body} ")
        print(f"Response Headers: {headers} ")
        print("Message Sent!")

        for post in new_posts:
            post.new_post=False
            post.save()
    except Exception as e:
        print("Error: {0}".format(e))

