import pytest

from django.contrib.auth.models import User

from django.urls import reverse
from django.utils import timezone

from blog.models import Post, PostComment, Direct_Message, Conversations


@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  assert User.objects.count() == 1

@pytest.mark.django_db
def test_home(client):
   url = reverse('post_list_v2', blogtype='alex')
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_community(client):
   url = reverse('post_list')
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_new_post_form(client, create_user, test_password):
   user = create_user(username='someone')
   url = reverse('post_new')
   client.login(
       username=user.username, password=test_password
   )
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_blog_post(client,create_user,test_password,auto_login_user):
   url = reverse('post_new')
   data = {
       'title': 'My Amazing Blog Post',
       'text': 'This is the best post ever'
   }
   client, test_user = auto_login_user()
   response = client.post(url, data=data)
   assert response.status_code == 302
   assert Post.objects.filter(pk=1).count() == 1
   assert Post.objects.filter(author=test_user).count() == 1

   assert Post.objects.filter(published_date__exact=None).count() == 0

@pytest.mark.django_db
def test_post_detail(client, create_user):
   user = create_user(username='someone')
   this_blog_post = Post.objects.create(title='hi', text='howdy', author=user, published_date=timezone.now())
   url = reverse('post_detail', kwargs={'pk': this_blog_post.pk})
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_edit_post_form(client, create_user, test_password):
   user = create_user(username='someone')
   client.login(
       username=user.username, password=test_password
   )
   this_blog_post = Post.objects.create(title='hi', text='howdy', author=user, published_date=timezone.now())
   url = reverse('post_edit', kwargs={'pk': this_blog_post.pk})
   response = client.get(url)
   assert response.status_code == 200
   data = {
      'title': this_blog_post.title+'LoL',
      'text': 'This is the best poster ever'
   }
   response = client.post(url, data)
   assert response.status_code == 302
   assert Post.objects.filter(pk=1).count() == 1
   assert Post.objects.filter(author=user).count() == 1
   assert Post.objects.filter(published_date__exact=None).count() == 0

@pytest.mark.django_db
def test_post_delete(client, create_user, test_password):
   user = create_user(username='someone')
   client.login(
      username=user.username, password=test_password
   )
   this_blog_post = Post.objects.create(title='hi', text='howdy', author=user, published_date=timezone.now())
   url = reverse('post_delete', kwargs={'pk': this_blog_post.pk})
   response = client.get(url)
   assert response.status_code == 302

@pytest.mark.django_db
def test_new_comment_form(client, create_user, test_password):
   user = create_user(username='someone')
   client.login(
       username=user.username, password=test_password
   )
   this_blog_post = Post.objects.create(title='hi', text='howdy', author=user, published_date=timezone.now())
   url = reverse('comment', kwargs={'pk': this_blog_post.pk})
   response = client.get(url)
   assert response.status_code == 200
   data = {
      'text': 'This is the best comment ever'
   }
   response = client.post(url, data)
   assert response.status_code == 302
   assert PostComment.objects.filter(pk=1).count() == 1
   assert PostComment.objects.filter(author=user).count() == 1
   assert PostComment.objects.filter(published_date__exact=None).count() == 0

@pytest.mark.django_db
def test_edit_comment_form(client, create_user, test_password):
   user = create_user(username='someone')
   client.login(
       username=user.username, password=test_password
   )
   this_blog_post = Post.objects.create(title='hi', text='howdy', author=user, published_date=timezone.now())
   this_comment = PostComment.objects.create(post=this_blog_post, text='hi', author=user, published_date=timezone.now())
   url = reverse('comment_edit', kwargs={'pk': this_comment.pk})
   response = client.get(url)
   assert response.status_code == 200
   data = {
      'text': this_comment.text+'This is the best poster ever'
   }
   response = client.post(url, data)
   assert response.status_code == 302
   assert PostComment.objects.filter(pk=1).count() == 1
   assert PostComment.objects.filter(author=user).count() == 1
   assert PostComment.objects.filter(published_date__exact=None).count() == 0

@pytest.mark.django_db
def test_comment_delete(client, create_user, test_password):
   user = create_user(username='someone')
   client.login(
      username=user.username, password=test_password
   )
   this_blog_post = Post.objects.create(title='hi', text='howdy', author=user, published_date=timezone.now())
   this_comment = PostComment.objects.create(post=this_blog_post, text='hi', author=user, published_date=timezone.now())
   url = reverse('comment_delete', kwargs={'pk': this_comment.pk})
   response = client.get(url)
   assert response.status_code == 302

@pytest.mark.django_db
def test_dm_list(client, create_user, test_password):
   user = create_user(username='someone')
   client.login(
      username=user.username, password=test_password
   )
   url = reverse('message_list')
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_dm_form(client, create_user, test_password, auto_login_user):
   url = reverse('direct_message')
   data = {
      'text': 'This is the best post ever'
   }
   client, test_user = auto_login_user()
   response = client.post(url, data=data)
   assert response.status_code == 302

@pytest.mark.django_db
def test_convo_detail(client, create_user, test_password):
   user1 = create_user(username='someone')
   user2 = create_user(username='noone')
   client.login(
      username=user1.username, password=test_password
   )
   this_convo = Conversations.objects.create()
   this_convo.recipient.add(user1, user2)
   this_convo.marked_as_new.add(user1, user2)
   this_convo.save()
   message = Direct_Message.objects.create(text='hi', author=user1, conversation=this_convo, send_date=timezone.now())
   url = reverse('conversation_detail', kwargs={'pk': this_convo.pk})
   response = client.get(url)
   assert response.status_code == 200
