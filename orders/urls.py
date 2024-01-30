from django.urls import path,include
from .views import *

urlpatterns = [
    path('create/', createOrderView.as_view()),
    path('getAll/',getAllOrders.as_view()),
    path('invoice/<int:order_id>/',GenerateInvoice.as_view()),
    path('my/',getRespectiveOrders.as_view()),
]