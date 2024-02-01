from rest_framework import status
from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(api_client):
    registerUrl = reverse('users:register')

    data = {
        'username': 'admin',
        'email': 'admin@example.com',
        'password': '12345566',
        'role': 'Admin'
    }

    registerResponse = api_client.post(registerUrl,data)
    email = registerResponse.data['user']['email']

    user = get_user_model().objects.get(email=email)
    return user

@pytest.fixture
def genre(api_client,admin_user):
    url = reverse('genres:create')
    api_client.force_authenticate(user=admin_user)

    data = {
        'name': 'testGenre',
        'description': 'testDescription'
    }

    response = api_client.post(url,data)
    genres =  response.data['genres']
    return genres[0]

# create genre
@pytest.mark.django_db
def test_createGenre(api_client,admin_user):
    url = reverse('genres:create')
    api_client.force_authenticate(user=admin_user)

    data = {
        'name': 'testGenre',
        'description': 'testDescription'
    }

    response = api_client.post(url,data)
    
    assert response.status_code == status.HTTP_200_OK
    assert 'genres' in response.data


@pytest.mark.django_db
def test_getGenre(api_client,admin_user):
    url = reverse('genres:genreview')
    api_client.force_authenticate(user=admin_user)

    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert 'genres' in response.data


@pytest.mark.django_db
def test_deleteGenre(api_client,admin_user,genre):
    url = reverse('genres:genreoperations', kwargs={'id': genre['id']})
    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert 'genres' in response.data


@pytest.mark.django_db
def test_updateGenre(api_client,admin_user,genre):
    url = reverse('genres:genreoperations', kwargs={'id': genre['id']})
    api_client.force_authenticate(user=admin_user)

    data={
        'name': 'horror'
    }

    response = api_client.put(url,data)
    
    assert response.status_code == status.HTTP_200_OK
    assert 'genres' in response.data


@pytest.mark.django_db
def test_getNamesApi(api_client,admin_user,genre):
    url = reverse('genres:names')
    api_client.force_authenticate(user=admin_user)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'genres' in response.data