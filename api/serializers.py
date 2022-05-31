from rest_framework.serializers import ModelSerializer

from api.models import Project
from authentication.serializers import UserSerializer


class ProjectSerializer(ModelSerializer):
    # author_user_id = UserSerializer()

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author_user_id']

