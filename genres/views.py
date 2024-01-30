from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# model imports
from .models import GenreModel
from .serializer import *

# Create your views here.
class createGenre(APIView):
    model = GenreModel
    serializer = createGenreSerializer
    permission_classes=[IsAuthenticated]

    def post(self,request):
        try:
            user = request.user
            data = request.data

            if user.role != 'Admin' and user.role != 'Seller':
                return Response({'message':'Permissions required'},status=403)
            
            genre = self.serializer(data=data)

            if not genre.is_valid():
                return Response({'error' : genre.error_messages,'message':'Invalid data'},status=400)
            
            print(genre.validated_data.get('name'))
            print(genre.validated_data.get('description'))

            name = str(genre.validated_data.get('name'))
            description = str(genre.validated_data.get('description'))
            db_genre,created = self.model.objects.get_or_create(name=name.lower(),description=description.lower())

            genres = self.model.objects.all()

            genres_list = [{'id': genre.id,'name': genre.name, 'description': genre.description} for genre in genres]

            return Response({
                'genres': genres_list
            },status=200)

        except Exception as err:
            return Response({'message': err.args},status=500)
        
class GenreView(APIView):
    model = GenreModel
    serializer = GenreSerialzer
    permission_classes=[IsAuthenticated]


    def get(self,request):
        try:
            genres = self.model.objects.all()

            genres_list = [{'id': genre.id,'name': genre.name, 'description': genre.description} for genre in genres]

            return Response({
                'genres': genres_list
            },status=200)
        except Exception as err:
            return Response({'message': err.args},status=500)
    
        
class GenreOperations(APIView):
    model = GenreModel
    serializer = GenreSerialzer
    permission_classes=[IsAuthenticated]


    def delete(self,request,id):
        try:

            genre = self.model.objects.get(id=id)
            genre.delete()

            genres = self.model.objects.all()

            genres_list = [{'id': genre.id,'name': genre.name, 'description': genre.description} for genre in genres]

            return Response({
                'genres': genres_list
            },status=200)

        except Exception as err:
            return Response({'message': err.args},status=500)
        
    def put(self,request,id):
        try:
            data = request.data
            
            genre = self.serializer(data=data)
            if not genre.is_valid():
                return Response({'message': genre.error_messages},status=400)
            

            db_genre = self.model.objects.get(id=id)

            name = genre.validated_data.get('name')
            description = genre.validated_data.get('description')

            if name is not None:
                db_genre.name = name
            
            if description is not None:
                db_genre.description = description

            db_genre.save()
            
            genres = self.model.objects.all()

            genres_list = [{'id': genre.id,'name': genre.name, 'description': genre.description} for genre in genres]

            return Response({
                'genres': genres_list
            },status=200)

        except Exception as err:
            return Response({'message': err.args},status=500)
        

class GenreNamesApi(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            genres = GenreModel.objects.all()
            genres_list = [genre.name for genre in genres]
            
            return Response({
                'genres': genres_list
            },status=200)

            return Response({'authors': author_names}, status=200)
        except Exception as err:
            return Response({'message': err.args},status=500)