from rest_framework.serializers import ModelSerializer

from api.models import Project
from authentication.serializers import UserSerializer


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']


class ProjectDetailSerializer(ModelSerializer):
    author_user_id = UserSerializer()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'date_created']

