from rest_framework.serializers import ModelSerializer

from api.models import Project, Contributor
from authentication.serializers import UserSerializer


# -------------------------------- Project --------------------------------

class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']


class ProjectDetailSerializer(ModelSerializer):
    author_user_id = UserSerializer()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'date_created']


# -------------------------------- Contributor --------------------------------

class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'project_id', 'role']
