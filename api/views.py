from django.db import transaction
from rest_framework import status, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import (Project,
                        Contributor,
                        Issue,
                        Comment)
from api.permissions import (IsContributor,
                             IsProjectAuthorOrContributorDetailsOrReadOnly,
                             IsProjectAuthorOrReadOnly,
                             IsIssueAuthorOrReadOnly,
                             IsCommentAuthorOrReadOnly)
from api.serializers import (ProjectDetailSerializer,
                             ProjectListSerializer,
                             ContributorListSerializer,
                             IssueListSerializer,
                             IssueDetailSerializer,
                             CommentListSerializer,
                             CommentDetailSerializer,
                             ContributorDetailSerializer)
from api.utils import validate_multiple_choice, is_digit_or_raise_exception


class MultipleSerializerMixin:
    """
    Choice of serializer according to the type of action.
    """
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super(MultipleSerializerMixin, self).get_serializer_class()


class DestroyMixin:
    """
    Behavior of the destroy method.
    """

    def destroy(self, request, model_name, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": f"{model_name} deleted successfully"
        },
            status=status.HTTP_200_OK)


# -------------------------------- Project --------------------------------

class ProjectViewset(MultipleSerializerMixin,
                     DestroyMixin,
                     ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthorOrContributorDetailsOrReadOnly]

    def get_queryset(self):
        if self.action == 'list':
            query = self.request.user
            contributors = [
                contributor.user for contributor in Contributor.objects.filter(user=query)
            ]
            return Project.objects.filter(author_user__in=contributors)
        return Project.objects.all()

    def create(self, request, *args, **kwargs):
        id_author = request.user.id
        type_choice = validate_multiple_choice(choices_list=Project.PROJECT_TYPE,
                                               user_choice=request.POST.get('type'))
        data = {
            "title": request.POST.get('title'),
            "description": request.POST.get('description'),
            "type": type_choice,
            "author_user": id_author,
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def perform_create(self, serializer):
        project = serializer.save()
        try:
            contributor = Contributor.objects.create(project=project,
                                                     user=project.author_user,
                                                     role='author')
        except TypeError:
            error_message = {
                'error': 'fail to create contributor',
            }
            raise exceptions.APIException(detail=error_message)
        contributor.save()

    def destroy(self, request, model_name="project", *args, **kwargs):
        return super().destroy(request, model_name, *args, **kwargs)


# -------------------------------- Contributor --------------------------------

class ContributorViewset(MultipleSerializerMixin,
                         DestroyMixin,
                         ModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsProjectAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'delete', ]

    def get_queryset(self):
        queryset = Contributor.objects.all()
        project_id = self.kwargs.get('project_pk')
        is_digit_or_raise_exception(project_id)

        if project_id is not None:
            queryset = Contributor.objects.filter(project=project_id)
        if not queryset:
            error_message = {
                "error": "This project does not exist",
            }
            raise exceptions.NotFound(detail=error_message)
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.POST.get('user')
        queryset = Contributor.objects.filter(user=user, project=self.kwargs.get('project_pk'))
        if queryset:
            error_message = {
                'error': 'This contributor already exist'
            }
            raise exceptions.ValidationError(detail=error_message)
        project = self.kwargs.get('project_pk')
        data = {
            "user": user,
            "project": project,
            "role": Contributor.ROLE_CHOICES[1][0],
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, model_name="contributor", *args, **kwargs):
        return super().destroy(request, model_name, *args, **kwargs)


# -------------------------------- Issue --------------------------------

class IssueViewset(MultipleSerializerMixin,
                   DestroyMixin,
                   ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsIssueAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete', ]

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        is_digit_or_raise_exception(project_id)
        get_object_or_404(Project, id=project_id)
        queryset = Issue.objects.filter(project=project_id)
        return queryset

    def create(self, request, *args, **kwargs):
        project = self.kwargs.get('project_pk')
        tag = validate_multiple_choice(choices_list=Issue.TAG_CHOICES,
                                       user_choice=request.POST.get('tag'))
        priority = validate_multiple_choice(choices_list=Issue.PRIORITY_CHOICES,
                                            user_choice=request.POST.get('priority'))
        status_choice = validate_multiple_choice(choices_list=Issue.STATUS_CHOICES,
                                                 user_choice=request.POST.get('status'))
        author_id = request.user.id
        assignee_id = request.POST.get('assignee_user')
        if assignee_id is None:
            assignee_id = author_id
        else:
            is_digit_or_raise_exception(assignee_id)

        data = {
            "title": request.POST.get('title'),
            "description": request.POST.get('description'),
            "tag": tag,
            "priority": priority,
            "project": project,
            "status": status_choice,
            "author_user": author_id,
            "assignee_user": assignee_id,
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        assignee_id = request.POST.get('assignee_user')
        if assignee_id is not None:
            is_digit_or_raise_exception(assignee_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, model_name="issue", *args, **kwargs):
        return super().destroy(request, model_name, *args, **kwargs)


# -------------------------------- Comment --------------------------------

class CommentViewset(MultipleSerializerMixin,
                     DestroyMixin,
                     ModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsCommentAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'delete', ]

    def get_queryset(self):
        queryset = Comment.objects.all()
        issue_id = self.kwargs.get('issue_pk')
        project_id = self.kwargs.get('project_pk')
        is_digit_or_raise_exception(issue_id)
        is_digit_or_raise_exception(project_id)
        get_object_or_404(Issue, id=issue_id)
        get_object_or_404(Project, id=project_id)

        if issue_id is not None:
            queryset = Comment.objects.filter(issue=issue_id)
        return queryset

    def create(self, request, *args, **kwargs):

        author_id = request.user.id
        issue_id = self.kwargs.get('issue_pk')

        data = {
            "description": request.POST.get('description'),
            "author_user": author_id,
            "issue": issue_id,
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        author_id = request.user.id
        issue_id = self.kwargs.get('issue_pk')
        data = {
            "description": request.POST.get('description'),
            "author_user": author_id,
            "issue": issue_id,
        }
        serializer = self.serializer_class(instance=instance,
                                           data=data,
                                           partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, model_name="comment", *args, **kwargs):
        return super().destroy(request, model_name, *args, **kwargs)
