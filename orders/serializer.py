from rest_framework import serializers
from .models import OrderModel
from users.models import CustomUser
from books.models import BookModel
from genres.models import GenreModel

class createOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ['user','books','is_paid','total_price']



# outside serializer
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreModel
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_active','is_staff','is_superuser','role']

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    class Meta:
        model = BookModel
        fields = ['id', 'title', 'cover_image_url', 'author', 'description', 'genre', 'price', 'published_by', 'is_available']


# common serializers
class getOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    books = BookSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ['id', 'user', 'books', 'order_date', 'total_price', 'is_paid']

class getMyOrderSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ['id', 'books', 'order_date', 'total_price', 'is_paid']