from django.contrib.auth.models import User
from user_manager.models import UserProfile
from user_manager.views import all_users
from .models import Post, PostComment
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from celery import shared_task
from datetime import datetime
import pytz

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
    if len(users) > 0:

        for user in users:
            if user.email_updates is True:
                email_user_list.append(user.user.email)
        for each_user in email_user_list:
            new_post_email(each_user)
        for post in new_posts:
            post.new_post = False
            post.save()


def new_post_email(email_address):
    new_posts = Post.objects.filter(new_post=True)
    this_message = "<ul>"
    for new_post in new_posts:
        this_message += f'<li><a href="{settings.SITE_URL}/post/{new_post.pk}">{new_post.title}</a></li>'
    this_message += "</ul>"
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email_address,
        subject='New Posts',
        # html_content=this_message
    )
    message.dynamic_template_data = {
        "new_posts": this_message
    }
    message.template_id = "d-3ad4b311d85241b0a0d3c02a3741eac0"

    try:
        sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response Code: {code} ")
        print(f"Response Body: {body} ")
        print(f"Response Headers: {headers} ")
        print("Message Sent!")

    except Exception as e:
        print("Error: {0}".format(e))

@ shared_task
def comment_emails(pk, email_address):
    new_comment = PostComment.objects.get(pk=pk)
    this_post = new_comment.post
    this_user = this_post.author.username


    post_url = f'{settings.SITE_URL}/post/{new_comment.pk}'
    commenter = new_comment.author.username
    comment_time = new_comment.published_date
    comment_time = comment_time.astimezone(pytz.timezone('America/New_York'))
    comment_time = comment_time.strftime("%I:%M %p")

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email_address,
        subject='New Comments',
        # html_content=this_message
    )
    message.dynamic_template_data = {
        "post_url": post_url,
        "commenter": commenter,
        "comment_time": comment_time,
        "this_user": this_user,
    }

    message.template_id = "d-08e5519f4f8a4bef9189d904eb02c91f"

    try:
        sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response Code: {code} ")
        print(f"Response Body: {body} ")
        print(f"Response Headers: {headers} ")
        print("Message Sent!")

    except Exception as e:
        print("Error: {0}".format(e))




