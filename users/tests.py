from rest_framework import status
from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()



@pytest.mark.django_db
def test_create_buyer(api_client):
    url = reverse('users:register')  # Assuming you have a 'register' URL in your app's urls.py

    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
        'role': 'Buyer'
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'user' in response.data

    user = get_user_model().objects.get(username='testuser')

    assert user.email == 'test@example.com'
    assert user.check_password('testpassword')
    assert user.role == 'Buyer'
    assert not user.is_staff
    assert not user.is_superuser
    assert user.is_active

@pytest.mark.django_db
def test_create_seller(api_client):
    url = reverse('users:register')  # Assuming you have a 'register' URL in your app's urls.py

    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
        'role': 'Seller'
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'user' in response.data

    user = get_user_model().objects.get(username='testuser')

    assert user.email == 'test@example.com'
    assert user.check_password('testpassword')
    assert user.role == 'Seller'
    assert not user.is_staff
    assert not user.is_superuser
    assert user.is_active


@pytest.mark.django_db
def test_create_admin(api_client):
    url = reverse('users:register')  # Assuming you have a 'register' URL in your app's urls.py

    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
        'role': 'Admin'
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'user' in response.data

    user = get_user_model().objects.get(username='testuser')

    assert user.email == 'test@example.com'
    assert user.check_password('testpassword')
    assert user.role == 'Admin'
    assert user.is_staff
    assert user.is_superuser
    assert user.is_active

@pytest.mark.django_db
def test_anonymousUser(api_client):
    url = reverse('users:register') 

    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
        'role': 'None'
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    


# login testcase
@pytest.mark.django_db
def test_login(api_client):
    registerUrl = reverse('users:register')
    loginUrl = reverse('users:login')

    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
        'role': 'Admin'
    }

    api_client.post(registerUrl, data, format='json')

    data = {
        'email': 'test@example.com',
        'password': 'testpassword'
    }


    response = api_client.post(loginUrl,data,format='json')

    user = response.data['user']

    assert response.status_code == status.HTTP_200_OK
    assert 'user' in response.data
    assert 'access_token' in response.data
    assert 'refresh_token' in response.data


# adminview
@pytest.mark.django_db
def test_adminGetUsers(api_client):
    url = reverse('users:admin')
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

    api_client.force_authenticate(user=user)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'users' in response.data