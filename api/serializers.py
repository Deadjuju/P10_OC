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

    def create(self, validated_data):
        user = validated_data['user']
        print(f"User: {user}")
        project = validated_data['project']
        role = validated_data['role']
        contributor = Contributor.objects.create(user=user,
                                                 project=project,
                                                 role=role)
        contributor.save()
        return contributor


# -------------------------------- Issue --------------------------------

class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'tag', 'priority',
            'project', 'status', 'author_user', 'assignee_user', 'date_created'
        ]

    def create(self, validated_data):
        issue = Issue.objects.create(**validated_data)
        issue.save()
        return issue


class IssueDetailSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'tag', 'priority',
            'project', 'status', 'author_user', 'assignee_user', 'date_created'
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
