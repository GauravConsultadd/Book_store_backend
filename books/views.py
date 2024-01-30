from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from rest_framework.parsers import MultiPartParser
import uuid
from urllib.parse import urlparse
# from django.contrib.staticfiles.templatetags.staticfiles import static

from .models import BookModel
from .serializer import *
from genres.models import GenreModel

# Create your views here.
class createBooksView(APIView):
    model = BookModel
    serializer = createBookSerializer
    permission_classes=[IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self,request):
        try:
            user = request.user
            data = request.data

            if user.role != 'Admin' and user.role != 'Seller':
                return Response({'message':'Permissions required'},status=403)
            
            book = self.serializer(data=data)

            if not book.is_valid():
                return Response({'message': book.error_messages},status=400)
            
            title = str(book.validated_data.get('title'))
            author = str(book.validated_data.get('author'))
            cover_image_url = book.validated_data.get('cover_image_url')
            genre = str(book.validated_data.get('genre'))
            description = str(book.validated_data.get('description'))
            price = int(book.validated_data.get('price'))


            db_genre = GenreModel.objects.get(name=genre)

            # uploading image to azure blob storage
            filename = cover_image_url.name
            file_upload_name = str(uuid.uuid4()) + filename

            # azure stuff
            storage_url = os.environ.get('AZURE_STORAGE_URL')
            container_name = os.environ.get('AZURE_STORAGE_CONTAINER')
            credential = DefaultAzureCredential()
            blob_service_client = BlobServiceClient(account_url = storage_url, credential=credential)
            container_client = blob_service_client.get_container_client(container_name)

            blob_client = container_client.get_blob_client(file_upload_name)

            # Upload the file to Azure Blob Storage
            blob_client.upload_blob(cover_image_url.read(), overwrite=True)
            blob_url = blob_client.url

            book,created = self.model.objects.get_or_create(title=title,author=author,cover_image_url=blob_url,genre=db_genre,description=description,price=price,published_by=request.user)

            books = self.model.objects.all()
            books_list = [{'id': book.id,'title': book.title, 'description': book.description,'author': book.author,'genre':   book.genre.name,'price': book.price,'cover_image_url': book.cover_image_url,'is_available': book.is_available} for book in books]

            inventory = self.model.objects.filter(published_by = request.user.id)
            json_inventory = [{'id': book.id,'title': book.title, 'description': book.description,'author': book.author,'genre':    book.genre.name,'price': book.price,'cover_image_url': book.cover_image_url,'is_available': book.is_available} for book in inventory]


            return Response({
                'message': 'Book created',
                'books': books_list,
                'inventory': json_inventory
            },status=201)

        except Exception as err:
            print(err.args)
            return Response({'message': err.args},status=500)
        

class BookView(APIView):
    model = BookModel
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            books = self.model.objects.all()
            books_list = [{'id': book.id,'title': book.title, 'description': book.description,'author': book.author,'genre':   book.genre.name,'price': book.price,'cover_image_url': book.cover_image_url,'is_available': book.is_available} for book in books]

            return Response({
                'books': books_list
            },status=200)

        except Exception as err:
            return Response({'message': err.args},status=500)
        

class InventoryOperation(APIView):
    model = BookModel
    permission_classes = [IsAuthenticated]
    serializer_class= updateBookSerializer
    parser_classes = (MultiPartParser,)

    def put(self,request,bookId):
        try:
            id = bookId
            data = request.data
            db_book = self.model.objects.get(id=id)

            request_book = self.serializer_class(data=data)

            if not request_book.is_valid():
                return Response({'message': request_book.error_messages},status=403)
            print("yaha")
            
            

            title = str(request_book.validated_data.get('title'))
            if title:
                db_book.title = title

            cover_image_url = request_book.validated_data.get('cover_image_url')
            if cover_image_url and cover_image_url != db_book.cover_image_url:
                # azure stuff
                parsed_url = urlparse(db_book.cover_image_url)
                blob_name = '/'.join(parsed_url.path.split('/')[2:])

                storage_url = os.environ.get('AZURE_STORAGE_URL')
                container_name = os.environ.get('AZURE_STORAGE_CONTAINER')
                credential = DefaultAzureCredential()
                blob_service_client = BlobServiceClient(account_url = storage_url, credential=credential)
                container_client = blob_service_client.get_container_client(container_name)

                # Delete the blob
                blob_client = container_client.get_blob_client(blob_name)
                blob_client.delete_blob()

                # ready file for upload
                filename = cover_image_url.name
                file_upload_name = str(uuid.uuid4()) + filename

                blob_client = container_client.get_blob_client(file_upload_name)

                # Upload the file to Azure Blob Storage
                blob_client.upload_blob(cover_image_url.read(), overwrite=True)
                blob_url = blob_client.url

                db_book.cover_image_url = blob_url

            author = request_book.validated_data.get('author')
            if author:
                db_book.author = author
            
            description = request_book.validated_data.get('description')
            if description:
                db_book.description = description
            
            genre = request_book.validated_data.get('genre')
            if(genre):
                db_genre = GenreModel.objects.get(name=genre)
                db_book.genre = db_genre

            price = request_book.validated_data.get('price')
            if price:
                db_book.price = price

            # request_book.save()
            db_book.save()

            books = self.model.objects.all()
            books_list = [{'id': book.id,'title': book.title, 'description': book.description,'author': book.author,'genre':   book.genre.name,'price': book.price,'cover_image_url': book.cover_image_url,'is_available': book.is_available} for book in books]

            inventory = self.model.objects.filter(published_by = request.user.id)
            json_inventory = [{'id': book.id,'title': book.title, 'description': book.description,'author': book.author,'genre':    book.genre.name,'price': book.price,'cover_image_url': book.cover_image_url,'is_available': book.is_available} for book in inventory]
            return Response({
                'books': books_list,
                'inventory': json_inventory
            },status=200)

            
        except Exception as err:
            return Response({'message': err.args},status=500)
        

    def delete(self,request,bookId):
        try:
            id = bookId
            data = request.data
            db_book = self.model.objects.get(id=id)

            # azure stuff
            parsed_url = urlparse(db_book.cover_image_url)
            blob_name = '/'.join(parsed_url.path.split('/')[2:])

            storage_url = os.environ.get('AZURE_STORAGE_URL')
            container_name = os.environ.get('AZURE_STORAGE_CONTAINER')
            credential = DefaultAzureCredential()
            blob_service_client = BlobServiceClient(account_url = storage_url, credential=credential)
            container_client = blob_service_client.get_container_client(container_name)

            # Delete the blob
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.delete_blob()

            db_book.delete()

            books = self.model.objects.all()
            books_list = [{'id': book.id,'title': book.title, 'description': book.description,'author': book.author,'genre':   book.genre.name,'price': book.price,'cover_image_url': book.cover_image_url,'is_available': book.is_available} for book in books]

            inventory = self.model.objects.filter(published_by = request.user.id)
            json_inventory = [{'id': book.id,'title': book.title, 'description': book.description,'author': book.author,'genre':    book.genre.name,'price': book.price,'cover_image_url': book.cover_image_url,'is_available': book.is_available} for book in inventory]
            return Response({
                'books': books_list,
                'inventory': json_inventory
            },status=200)


        except Exception as err:
            return Response({'message': err.args},status=500)

class Inventory(APIView):
    permission_classes=[IsAuthenticated]
    model = BookModel

    def get(self,request):
        try:
            books = self.model.objects.filter(published_by = request.user.id)
            books_list = [{'id': book.id,'title': book.title, 'description': book.description,'author': book.author,'genre':   book.genre.name,'price': book.price,'cover_image_url': book.cover_image_url,'is_available': book.is_available} for book in books]

            return Response({
                'books': books_list
            },status=200)
        except Exception as err:
            return Response({'message': err.args})
        

class AuthorNamesAPIView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            authors = BookModel.objects.values_list('author', flat=True).distinct()
            author_names = list(authors)

            return Response({'authors': author_names}, status=200)
        except Exception as err:
            return Response({'message': err.args},status=500)
        
        
class BookSearchAPIView(APIView):

    def post(self, request):
        try:
            search_text = request.data.get('searchText', '')
            genres = request.data.get('genres', [])
            authors = request.data.get('authors', [])
            print(authors,genres,search_text)

            queryset = BookModel.objects.all()

            if search_text:
                queryset = queryset.filter(title__icontains=search_text)

            if genres:
                queryset = queryset.filter(genre__name__in=genres)

            if authors:
                queryset = queryset.filter(author__in=authors)

            books_list = [{'id': book.id,'title': book.title, 'description': book.description,'author': book.author,'genre':    book.genre.name,'price': book.price,'cover_image_url': book.cover_image_url,'is_available': book.is_available} for book in queryset]        
            return Response({'books': books_list},status=200)
        except Exception as err:
            return Response({'message': err.args},status=500)
        

class CheckAzureCredentials(APIView):
    def get(self,request):
        try:
            vault_url = os.environ.get('AZURE_VAULT_URL')
            secret_name = "ExampleKey"

            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=vault_url, credential=credential)
            secret = client.get_secret(secret_name)
            print(secret.value)

            return Response({
                'message': secret.value
            })
        except Exception as err:
            return Response({'message': err.args},status=500)
        

class CheckAzureBlobStorage(APIView):
    def get(self,request):
        try:
            storage_url = os.environ.get('AZURE_STORAGE_URL')
            container_name = os.environ.get('AZURE_STORAGE_CONTAINER')
            credential = DefaultAzureCredential()
            blob_service_client = BlobServiceClient(account_url = storage_url, credential=credential)
            container_client = blob_service_client.get_container_client(container = container_name)
            blob_client = container_client.get_blob_client(blob = "61jCkOVf1oL._SY522_.jpg")
            data = blob_client.download_blob().readAll()
            print(data)

            return Response({
                'message': 'done'
            })
        except Exception as err:
            return Response({'message': err.args},status=500)
        