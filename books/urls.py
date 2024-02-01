from django.urls import path,include
from .views import *

app_name = 'books'

urlpatterns = [
    path('create/', createBooksView.as_view(),name='create'),
    path('', BookView.as_view(),name='book_view'),
    path('inventory/', Inventory.as_view(),name='inventory'),
    path('<int:bookId>/', InventoryOperation.as_view(),name='inventoryOps'),
    path('authors/', AuthorNamesAPIView.as_view(),name='authors'),
    path('search/', BookSearchAPIView.as_view(),name='search'),
    path('storage/', CheckAzureBlobStorage.as_view(),name='search'),
]