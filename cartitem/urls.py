from django.urls import path
from .views import *

app_name = 'carts'

urlpatterns = [
    path('', cartOperations.as_view(),name='cartOps'),
    path('<int:id>/', CartItemView.as_view(),name='cart'),
]