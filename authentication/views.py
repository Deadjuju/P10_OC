from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import get_user_model

from authentication.serializers import UserSerializer


User = get_user_model()


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
