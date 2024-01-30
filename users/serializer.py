from django.shortcuts import render
from rest_framework import serializers
from .models import CustomUser

# Create your views here.
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4, max_length=20, required=True)
    email = serializers.EmailField(min_length=8, max_length=80, required=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    role = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields='__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(min_length=4, max_length=20, required=True)
    password = serializers.CharField(min_length=8, required=True)
