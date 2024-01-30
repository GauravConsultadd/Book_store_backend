from django.urls import path,include
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('check/',Checker.as_view()),
    path('logout/',Logout.as_view()),
    # path('',LoadUser.as_view()),
    path('getCurrentUser/',GetCurrentUser.as_view()),
    path('admin/',AdminView.as_view()),
]