from rest_framework.serializers import ModelSerializer

from api.models import Project, Contributor, Issue, Comment
from authentication.serializers import UserSerializer


# -------------------------------- Project --------------------------------

class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']
        extra_kwargs = {
            'author_user_id': {'write_only': True},
            'description': {'write_only': True},
        }

    def create(self, validated_data):
        title = validated_data['title']
        description = validated_data['description']
        type = validated_data['type']
        author_user_id = validated_data["author_user_id"]
        project = Project.objects.create(**validated_data)
        project.save()
        return project


class ProjectDetailSerializer(ModelSerializer):
    author_user_id = UserSerializer()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'date_created']


# -------------------------------- Contributor --------------------------------

class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']


# -------------------------------- Issue --------------------------------

class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'tag', 'priority',
            'project_id', 'status', 'author_user_id', 'assignee_user_id', 'date_created'
        ]


class IssueDetailSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'tag', 'priority',
            'project_id', 'status', 'author_user_id', 'assignee_user_id', 'date_created'
        ]


# -------------------------------- Comment --------------------------------

class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'description', 'author_user_id', 'issue_id'
        ]


class CommentDetailSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'description', 'author_user_id', 'issue_id', 'date_created'
        ]
