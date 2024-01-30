from django.db import models
from users.models import CustomUser
from books.models import BookModel

# Create your models here.
class OrderModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    books = models.ManyToManyField(BookModel)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    pdf_invoice = models.FileField(upload_to='invoices/', null=True, blank=True)