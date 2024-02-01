from django.urls import path,include
from .views import *

app_name = 'orders'

urlpatterns = [
    path('create/', createOrderView.as_view(),name='create'),
    path('getAll/',getAllOrders.as_view(),name='getAll'),
    path('invoice/<int:order_id>/',GenerateInvoice.as_view()),
    path('my/',getRespectiveOrders.as_view(),name='my'),
]