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
        'username': 'Seller',
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
        'name': 'testGenre',
        'description': 'testDescription'
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
        'title':'titleBook',
        'description':'bookDescription',
        'cover_image_url': image,
        'author': 'bookAuthor',
        'genre': genre['name'],
        'price': '29'
    }

    response = api_client.post(url,data)

    return response.data['books'][0]    


# create book view
@pytest.mark.django_db
def test_createBook(api_client,admin_user,genre):
    url = reverse('books:create')
    api_client.force_authenticate(admin_user)

    image_content = b'Test image content'
    image = SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")


    data = {
        'title':'titleBook',
        'description':'bookDescription',
        'cover_image_url': image,
        'author': 'bookAuthor',
        'genre': genre['name'],
        'price': '29'
    }

    response = api_client.post(url,data)
    # print(response.message)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'books' in response.data
    assert 'inventory' in response.data

    # deleting the file
    book = response.data['books'][0]
    url = reverse('books:inventoryOps',kwargs={'bookId': book['id']})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'books' in response.data


@pytest.mark.django_db
def test_BookView(api_client,admin_user):
    url = reverse('books:book_view')
    api_client.force_authenticate(admin_user)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'books' in response.data


@pytest.mark.django_db
def test_BookInventory(api_client,admin_user):
    url = reverse('books:inventory')
    api_client.force_authenticate(admin_user)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'books' in response.data


@pytest.mark.django_db
def test_deleteBook(api_client,admin_user,book):
    url = reverse('books:inventoryOps',kwargs={'bookId': book['id']})
    api_client.force_authenticate(admin_user)

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'books' in response.data


@pytest.mark.django_db
def test_updateBook(api_client,admin_user,book,genre):
    url = reverse('books:inventoryOps',kwargs={'bookId': book['id']})
    api_client.force_authenticate(admin_user)

    image_content = b'Test image'
    image = SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")

    data = {
        'title':'titleBook',
        'description':'bookDescription',
        'cover_image_url': image,
        'author': 'bookAuthor',
        'genre': genre['name'],
        'price': '29'
    }

    response = api_client.put(url,data)

    assert response.status_code == status.HTTP_200_OK
    assert 'books' in response.data
    assert 'inventory' in response.data

    # deleting the file
    book = response.data['books'][0]
    url = reverse('books:inventoryOps',kwargs={'bookId': book['id']})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'books' in response.data    
    

@pytest.mark.django_db
def test_bookAuthors(api_client,admin_user):
    url = reverse('books:authors')
    api_client.force_authenticate(admin_user)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'authors' in response.data