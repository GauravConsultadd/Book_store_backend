from django.db import models
from genres.models import GenreModel
from users.models import CustomUser

# Create your models here.
class BookModel(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    genre = models.ForeignKey(GenreModel, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    published_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    cover_image_url = models.FileField(upload_to='images/',null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)