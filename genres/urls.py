from django.urls import path,include
from .views import *

app_name='genres'

urlpatterns = [
    path('create/', createGenre.as_view(),name='create'),
    path('',GenreView.as_view(),name='genreview'),
    path('<int:id>/',GenreOperations.as_view(),name='genreoperations'),
    path('names/',GenreNamesApi.as_view(),name='names'),
]