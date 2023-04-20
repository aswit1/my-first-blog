import pytest
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from polls.models import Poll, Pollv2, PollQ


@pytest.mark.django_db
def test_new_poll_form(client, create_user, test_password):
   user = create_user(username='someone')
   url = reverse('poll_createv2')
   client.login(
       username=user.username, password=test_password
   )
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_new_poll_post(client,create_user,test_password, auto_login_user):
   url = reverse('poll_createv2')
   data = {
       'title': 'My Amazing Blog Poll',
       'description': 'This is the best poll ever'
   }
   client, test_user = auto_login_user()
   response = client.post(url, data=data)
   assert response.status_code == 302
   assert Pollv2.objects.filter(pk=1).count() == 1
   assert Pollv2.objects.filter(author=test_user).count() == 1
   assert Pollv2.objects.filter(published_date__exact=None).count() == 0

@pytest.mark.django_db
def test_pollv2_list(client):
   url = reverse('pollv2_list')
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_poll_detail(client, create_user):
   user = create_user(username='someone')
   this_poll = Pollv2.objects.create(title='hi', description='howdy', author=user, published_date=timezone.now())
   url = reverse('poll_detailv2', kwargs={'pk': this_poll.pk})
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_edit_poll_form(client, create_user, test_password):
   user = create_user(username='someone')
   client.login(
       username=user.username, password=test_password
   )
   this_poll = Pollv2.objects.create(title='hi', description='howdy', author=user, published_date=timezone.now())
   url = reverse('poll_edit', kwargs={'pk': this_poll.pk})
   response = client.get(url)
   assert response.status_code == 200
   data = {
      'title': this_poll.title+'LoL',
      'description': 'This is the best poster ever'
   }
   response = client.post(url, data)
   assert response.status_code == 302
   assert Pollv2.objects.filter(pk=1).count() == 1
   assert Pollv2.objects.filter(author=user).count() == 1
   assert Pollv2.objects.filter(published_date__exact=None).count() == 0

@pytest.mark.django_db
def test_poll_delete(client, create_user, test_password):
   user = create_user(username='someone')
   client.login(
      username=user.username, password=test_password
   )
   this_poll = Pollv2.objects.create(title='hi', description='howdy', author=user, published_date=timezone.now())
   url = reverse('poll_delete', kwargs={'pk': this_poll.pk})
   response = client.get(url)
   assert response.status_code == 302

@pytest.mark.django_db
def test_new_options(client, create_user, test_password):
   user = create_user(username='someone')
   client.login(
       username=user.username, password=test_password
   )
   this_poll =Pollv2.objects.create(title='hi', description='howdy', author=user, published_date=timezone.now())
   url = reverse('add_options', kwargs={'pk': this_poll.pk})
   response = client.get(url)
   assert response.status_code == 200
   data = {
      'description': 'This is the best comment ever'
   }
   response = client.post(url, data)
   assert response.status_code == 302
   assert PollQ.objects.filter(pk=1).count() == 1
   assert PollQ.objects.filter(votes=0).count() == 1

@pytest.mark.django_db
def test_options_delete(client, create_user, test_password):
   user = create_user(username='someone')
   client.login(
      username=user.username, password=test_password
   )
   this_poll = Pollv2.objects.create(title='hi', description='howdy', author=user, published_date=timezone.now())
   this_option = PollQ.objects.create(poll=this_poll, description='hi', votes=0)
   url = reverse('options_delete', kwargs={'pk': this_option.pk})
   response = client.get(url)
   assert response.status_code == 302

@pytest.mark.django_db
def test_poll_vote(client, create_user, test_password):
   user = create_user(username='someone')
   client.login(
      username=user.username, password=test_password
   )
   this_poll = Pollv2.objects.create(title='hi', description='howdy', author=user, published_date=timezone.now())
   this_option = PollQ.objects.create(poll=this_poll, description='hi', votes=0)
   url = reverse('poll_vote', kwargs={'pk': this_option.pk})
   response = client.get(url)
   assert response.status_code == 200
   data = {
      'vote': +1
   }
   response = client.post(url, data)
   assert response.status_code == 200
   assert PollQ.objects.filter(pk=1).count() == 1

