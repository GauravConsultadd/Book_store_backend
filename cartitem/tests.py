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
        'username': 'seller',
        'email': 'buyer@example.com',
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
        'name': 'testGenre1',
        'description': 'testDescription1'
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
        'title':'titleBook1',
        'description':'bookDescription1',
        'cover_image_url': image,
        'author': 'bookAuthor',
        'genre': genre['name'],
        'price': '29'
    }

    response = api_client.post(url,data)

    return response.data['books'][0] 

@pytest.fixture
def cart(api_client,admin_user,book):
    url = reverse('carts:cartOps')
    api_client.force_authenticate(admin_user)

    data = {
        'userId': admin_user.id,
        'bookId': book['id'],
        'price': 50,
        'quantity': 1
    }

    response = api_client.post(url,data)
    carts = response.data['cart']
    return carts[0]


@pytest.mark.django_db
def test_createCart(api_client,admin_user,book):
    url = reverse('carts:cartOps')
    api_client.force_authenticate(admin_user)

    data = {
        'userId': admin_user.id,
        'bookId': book['id'],
        'price': 50,
        'quantity': 1
    }

    response = api_client.post(url,data)

    assert response.status_code == status.HTTP_200_OK
    assert 'cart' in response.data


@pytest.mark.django_db
def test_getUserCart(api_client,admin_user):
    url = reverse('carts:cartOps')
    api_client.force_authenticate(admin_user)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'cart' in response.data


@pytest.mark.django_db
def test_deleteCart(api_client,admin_user,cart):
    url = reverse('carts:cart',kwargs={'id': cart['id']})
    api_client.force_authenticate(admin_user)

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'cart' in response.data