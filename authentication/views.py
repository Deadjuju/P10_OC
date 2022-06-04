from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# from authentication.models import User
from django.contrib.auth import get_user_model

from authentication.serializers import UserSerializer


User = get_user_model()


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        print(f"REQUEST: {request.data}")
        print('"' * 80)
        # data = {
        #     "email": request.data.get('email'),
        #     "first_name": request.POST.get('first_name'),
        #     "last_name": request.POST.get('last_name'),
        #     "password": request.POST.get('password')
        # }
        data = request.data
        print("DATA")
        print(data)
        serializer = self.serializer_class(data=data)
        print(f"USER: {serializer}")
        print("-" * 90)
        print(f"Serializer: {serializer}")
        print(serializer.is_valid())
        if serializer.is_valid():
            print("It is VALID!!!")
            serializer.save()
            print("User created correctly | From views")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("BYEBYE!!!!!!!!")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

