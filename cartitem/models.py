from django.db import models
from users.models import CustomUser
from books.models import BookModel

# Create your models here.
class CartItemModel(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()