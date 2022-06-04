from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Project, Contributor, Issue, Comment
from api.serializers import (ProjectDetailSerializer,
                             ProjectListSerializer,
                             ContributorSerializer,
                             IssueListSerializer,
                             IssueDetailSerializer,
                             CommentListSerializer,
                             CommentDetailSerializer)


User = get_user_model()


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            query = self.request.user
            return Project.objects.filter(author_user_id=query.id)
        return Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super(ProjectViewset, self).get_serializer_class()

    # def list(self, request, *args, **kwargs):
    #     query = request.user
    #     query_set = Project.objects.filter(author_user_id=query.id)
    #     return Response(self.serializer_class(query_set, many=True).data,
    #                     status=status.HTTP_200_OK)


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        queryset = Contributor.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = Contributor.objects.filter(project_id=project_id)
        return queryset


class IssueViewset(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = Issue.objects.filter(project_id=project_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super(IssueViewset, self).get_serializer_class()


class CommentViewset(ModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = Comment.objects.filter(issue_id=issue_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super(CommentViewset, self).get_serializer_class()

