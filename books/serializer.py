from rest_framework import serializers
from .models import BookModel

class createBookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=100)
    cover_image_url = serializers.FileField()
    genre = serializers.CharField()
    description = serializers.CharField(max_length=1000)
    price = serializers.IntegerField()

    class Meta:
        model = BookModel
        fields=('title','author','cover_image_url','description','genre','price')


class updateBookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255,required=False)
    author = serializers.CharField(max_length=100,required=False)
    cover_image_url = serializers.URLField(required=False)
    genre = serializers.CharField(required=False)
    description = serializers.CharField(max_length=1000,required=False)
    price = serializers.IntegerField(required=False)

    class Meta:
        model = BookModel
        fields = ('title','author','cover_image_url','description','genre','price')