import pytest
from django.urls import reverse
from user_manager.models import UserProfile

@pytest.mark.django_db
def test_user_detail(client, create_user, django_user_model, test_password):
    user = create_user(username='someone')
    client.login(
        username=user.username, password=test_password
    )
    url = reverse('this_user')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_all_users_detail(client, create_user, django_user_model, test_password):
    user = create_user(username='someone')
    client.login(
        username=user.username, password=test_password
    )
    url = reverse('all_users')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_profile_edit(client, create_user, test_password):
    user = create_user(username='someone')
    client.login(
        username=user.username, password=test_password
    )
    url = reverse('user_profile_edit')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_profile_edit_post(client, create_user, test_password):
    user = create_user(username='someone')
    client.login(
        username=user.username, password=test_password
    )
    url = reverse('user_profile_edit')
    response = client.post(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_admin_edit_users(client, create_user, test_password):
    user = create_user(username='someone')
    client.login(
        username=user.username, password=test_password
    )
    this_user = UserProfile.objects.create(user=user, birthday='2000-02-20', gender='female', phone_number='1231231234')
    url = reverse('user_edit', kwargs={'pk': this_user.pk})
    response = client.get(url)
    assert response.status_code == 200
    data = {
        'user': user,
        'birthday': '2001-01-10',
        'gender': 'female',
        'phone_number': '1234567890'

    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert UserProfile.objects.filter(pk=1).count() == 1

@pytest.mark.django_db
def test_user_delete(client, create_user, test_password):
    user = create_user(username='someone')
    client.login(
        username=user.username, password=test_password
    )
    this_user = UserProfile.objects.create(user=user, birthday='2000-02-20', gender='female', phone_number='1231231234')
    url = reverse('user_delete', kwargs={'pk': this_user.pk})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_registration(create_user, test_password, client):
    user = create_user(username='someone')
    client.login(
        username=user.username, password=test_password
    )
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200

