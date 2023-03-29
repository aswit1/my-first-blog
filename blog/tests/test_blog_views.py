import pytest

from django.contrib.auth.models import User
from blog.models import Post
from django.urls import reverse


@pytest.mark.django_db
def test_post_create(client):
  test_user = User.objects.create(username='someone', password='password')
  client.login(
      username=test_user.username, password='password'
  )
  Post.objects.create(author=test_user,title="My Awesome Title",text="Post text" )
  assert User.objects.count() == 1
  assert Post.objects.count() == 1


@pytest.mark.django_db
def test_post_create_v2(client,create_user,test_password):
  test_user = create_user(username='someone')
  client.login(username=test_user.username, password=test_password)
  Post.objects.create(author=test_user,title="My Awesome Title 2",text="Post text" )
  assert User.objects.count() == 1
  assert Post.objects.count() == 1


@pytest.mark.django_db
def test_post_create_v3(client,create_user,test_password,auto_login_user):
  client, test_user = auto_login_user()
  Post.objects.create(author=test_user,title="My Awesome Title 3",text="Post text" )
  assert User.objects.count() == 1
  assert Post.objects.count() == 1


@pytest.mark.django_db
def test_post_submit(client,create_user,test_password,auto_login_user):
  client, test_user = auto_login_user()
  Post.objects.create(author=test_user,title="My Awesome Title 3",text="Post text" )
  assert User.objects.count() == 1
  assert Post.objects.count() == 1



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

#
# @pytest.mark.django_db
# def test_unauthorized(client):
#    url = '/admin'
#    response = client.get(url)
#    assert response.status_code == 401
#
#
# @pytest.mark.django_db
# def test_superuser_view(admin_client):
#    url = '/admin'
#    response = admin_client.get(url)
#    assert response.status_code == 200