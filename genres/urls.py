from django.urls import path,include
from .views import *

urlpatterns = [
    path('create/', createGenre.as_view()),
    path('',GenreView.as_view()),
    path('<int:id>/',GenreOperations.as_view()),
    path('names/',GenreNamesApi.as_view()),
]