from rest_framework import serializers
from .models import GenreModel

class createGenreSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    class Meta:
        model = GenreModel
        fields = ('name','description')

class GenreSerialzer(serializers.Serializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = GenreModel
        fields ='__all__'

