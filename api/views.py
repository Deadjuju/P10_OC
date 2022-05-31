from rest_framework.viewsets import ModelViewSet

from api.models import Project
from api.serializers import ProjectSerializer


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
