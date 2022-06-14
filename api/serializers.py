from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer

from api.models import Project, Contributor, Issue, Comment
from authentication.serializers import UserSerializer


User = get_user_model()


# -------------------------------- Project --------------------------------

class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user']
        extra_kwargs = {
            'author_user': {'write_only': True},
            'description': {'write_only': True},
        }

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise ValidationError('Project already exists')
        return value

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        project.save()
        return project


class ProjectDetailSerializer(ModelSerializer):
    author_user = UserSerializer()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user', 'date_created']


# -------------------------------- Contributor --------------------------------

class ContributorListSerializer(ModelSerializer):
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


class ContributorDetailSerializer(ModelSerializer):
    project = ProjectDetailSerializer()
    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']


# -------------------------------- Issue --------------------------------

class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'tag', 'priority',
            'project', 'status', 'author_user', 'assignee_user',
        ]
        extra_kwargs = {
            'date_created': {'write_only': True},
        }

    @classmethod
    def check_if_assignee_is_contributor(cls,
                                         assignee: User,
                                         project: Project):
        """
        Raise an exceptions if assignee is not in contributor's list
        """
        assignee = get_object_or_404(User, pk=assignee.id)
        contributors = [
            contrib.user for contrib in Contributor.objects.filter(project=project)
        ]
        if assignee not in contributors:
            raise exceptions.ValidationError(
                detail=f"- {assignee} - This contributor is not part of the project."
            )

    def create(self, validated_data):
        self.check_if_assignee_is_contributor(assignee=validated_data['assignee_user'],
                                              project=validated_data['project'])
        issue = Issue.objects.create(**validated_data)
        return issue

    def update(self, instance, validated_data):
        super(IssueListSerializer, self).update(instance, validated_data)

        if validated_data.get("assignee_user") is not None:
            assignee = validated_data['assignee_user']
            self.check_if_assignee_is_contributor(assignee=assignee,
                                                  project=instance.project)
            instance.assignee_user = get_object_or_404(User, pk=assignee.id)

        instance.save()
        return instance


class IssueDetailSerializer(ModelSerializer):
    project = ProjectDetailSerializer()
    author_user = UserSerializer()
    assignee_user = UserSerializer()

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'tag', 'priority',
            'project', 'status', 'author_user', 'assignee_user',
            'date_created', 'date_updated',
        ]


# -------------------------------- Comment --------------------------------

class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id', 'description', 'author_user', 'issue',
        ]
        extra_kwargs = {
            'author_user': {'write_only': True},
            'issue': {'write_only': True},
        }


class CommentDetailSerializer(ModelSerializer):
    author_user = UserSerializer()
    issue = IssueDetailSerializer()

    class Meta:
        model = Comment
        fields = [
            'id', 'description', 'author_user', 'issue', 'date_created',
        ]
