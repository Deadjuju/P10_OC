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
        print("SERIALIZOR!!!")
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data["password"]
        user = User.objects.create(**validated_data)  # saving user object
        # user = User.objects.create_user(**validated_data)  # saving user object
        user.set_password(validated_data["password"])
        user.save()
        print("SAVE!!!")
        return user

        # def create(self, validated_data):
        #     print("COUCOU")
        #     user = User(
        #         email=validated_data['email'],
        #         first_name=validated_data['first_name'],
        #         last_name=validated_data['last_name'],
        #     )
        #     user.set_password(validated_data["password"])
        #     user.save()
        #     print("bye!")
        #     return user
