from django.contrib.auth import get_user_model
from rest_framework import status, exceptions
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
from api.utils import validate_multiple_choice, is_digit_or_raise_exception

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

    def create(self, request, *args, **kwargs):
        print("*" * 85)
        # data = request.data
        id_author = request.user.id
        type = validate_multiple_choice(choices_list=Project.PROJECT_TYPE,
                                        user_choice=request.POST.get('type'))
        data = {
            "title": request.POST.get('title', ''),
            "description": request.POST.get('description', ''),
            "type": type,
            "author_user_id": id_author,
        }
        serializer = self.serializer_class(data=data,
                                           context={'author_user_id': id_author})
        if serializer.is_valid():
            project = serializer.save()
            contributor = Contributor.objects.create(project=project,
                                                     user=request.user,
                                                     role='author')
            contributor.save()
            print("The project has been saved.")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Invalid serializer!!!")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------- Contributor --------------------------------

class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', ]

    def get_queryset(self):
        queryset = Contributor.objects.all()

        project_id = self.kwargs.get('project_pk')
        is_digit_or_raise_exception(project_id)

        if project_id is not None:
            queryset = Contributor.objects.filter(project=project_id)
        if not queryset:
            raise exceptions.NotFound(detail="This project does not exist")
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.POST.get('user')
        queryset = Contributor.objects.filter(user=user)
        if queryset:
            raise exceptions.ValidationError(detail="This contributor already exist")
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Contributor deleted successfully"
        },
            status=status.HTTP_200_OK)


# -------------------------------- Issue --------------------------------

class IssueViewset(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()

        project_id = self.kwargs.get('project_pk')
        is_digit_or_raise_exception(project_id)

        if project_id is not None:
            queryset = Issue.objects.filter(project_id=project_id)
        if not queryset:
            raise exceptions.NotFound(detail="This project does not exist")
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super(IssueViewset, self).get_serializer_class()

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
        is_digit_or_raise_exception(assignee_id)

        # Check if the assignee is a contributor
        contributors_id = [contrib.user.id for contrib in Contributor.objects.filter(project=project)]
        if assignee_id in contributors_id:
            assignee = assignee_id
        else:
            assignee = author_id

        data = {
            "title": request.POST.get('title'),
            "description": request.POST.get('description'),
            "tag": tag,
            "priority": priority,
            "project": project,
            "status": status_choice,
            "author_user": author_id,
            "assignee_user": assignee,
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
