from django.urls import reverse
from rest_framework import status
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(api_client):
    registerUrl = reverse('users:register')

    data = {
        'username': 'buyer',
        'email': 'seller@example.com',
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
        'name': 'testGenre2',
        'description': 'testDescription2'
    }

    response = api_client.post(url,data)
    genres =  response.data['genres']
    return genres[0]

@pytest.fixture
def book(api_client,admin_user,genre):
    url = reverse('books:create')
    api_client.force_authenticate(admin_user)

    image_content = b'Test image content'
    image = SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")


    data = {
        'title':'titleBook2',
        'description':'bookDescription2',
        'cover_image_url': image,
        'author': 'bookAuthor',
        'genre': genre['name'],
        'price': '29'
    }

    response = api_client.post(url,data)

    return response.data['books'][0] 


@pytest.mark.django_db
def test_createOrder(api_client,admin_user,book):
    url = reverse('orders:create')
    api_client.force_authenticate(admin_user)

    data = {
        'user': admin_user.id,
        'books': [ book['id'] ],
        'is_paid': True,
        'total_price': 150
    }

    response = api_client.post(url,data)
    assert response.status_code == status.HTTP_200_OK
    assert 'orders' in response.data


@pytest.mark.django_db
def test_getAllOrders(api_client,admin_user):
    url = reverse('orders:getAll')
    api_client.force_authenticate(admin_user)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'orders' in response.data


@pytest.mark.django_db
def test_getMyOrders(api_client,admin_user):
    url = reverse('orders:my')
    api_client.force_authenticate(admin_user)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'orders' in response.data