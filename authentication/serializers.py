from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

# from authentication.models import User
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data["password"]
        user = User.objects.create_user(**validated_data)
        user.save()
        print("User created correctly")
        return user
