import pytest
from django.urls import reverse



@pytest.mark.django_db
def test_user_detail(client, create_user, django_user_model, test_password):
    user = create_user(username='someone')
    client.login(
        username=user.username, password=test_password
    )
    url = reverse('this_user')
    response = client.get(url)
    assert response.status_code == 200
    # assert 'someone' in response.content


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