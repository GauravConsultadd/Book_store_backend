from django.urls import path,include
from .views import *

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('check/',Checker.as_view()),
    path('logout/',Logout.as_view()),
    # path('',LoadUser.as_view()),
    path('getCurrentUser/',GetCurrentUser.as_view()),
    path('admin/',AdminView.as_view(),name='admin'),
    path('role/', RoleChange.as_view(),name="role"),
    path('forgot/', ForgotPassword.as_view(),name="forgot"),
    path('reset/<str:uidb64>/<str:token>/', ResetPassword.as_view(),name="reset"),
]