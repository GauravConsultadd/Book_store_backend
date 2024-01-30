from rest_framework import serializers
from .models import CartItemModel

class createCartSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    bookId = serializers.IntegerField()
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItemModel
        fields = ('userId','bookId','price','quantity')
