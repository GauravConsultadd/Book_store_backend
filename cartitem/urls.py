from django.urls import path
from .views import *

urlpatterns = [
    path('', cartOperations.as_view()),
    path('<int:id>/', CartItemView.as_view()),
]