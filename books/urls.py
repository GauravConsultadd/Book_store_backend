from django.urls import path,include
from .views import *

urlpatterns = [
    path('create/', createBooksView.as_view()),
    path('', BookView.as_view()),
    path('inventory/', Inventory.as_view()),
    path('<int:bookId>/', InventoryOperation.as_view()),
    path('<int:bookId>/', InventoryOperation.as_view()),
    path('authors/', AuthorNamesAPIView.as_view()),
    path('search/', BookSearchAPIView.as_view()),
    path('keyvault/', CheckAzureCredentials.as_view()),
    path('storage/', CheckAzureBlobStorage.as_view()),
]