from django.urls import path, include
from rest_framework_nested import routers

from api.views import ProjectViewset, ContributorViewset, IssueViewset

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewset, basename='projects')

# Add users and issues to project path
project_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
project_router.register(r'users', ContributorViewset, basename='users')
project_router.register(r'issues', IssueViewset, basename='issues')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(project_router.urls)),
]
