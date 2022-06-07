from django.urls import path, include
from rest_framework_nested import routers

from api.views import ProjectViewset, ContributorViewset, IssueViewset, CommentViewset

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewset, basename='projects')

# Add users and issues to project path
project_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
project_router.register(r'users', ContributorViewset, basename='users')
project_router.register(r'issues', IssueViewset, basename='issues')

# Add comments to issue path
issue_router = routers.NestedSimpleRouter(project_router, r'issues', lookup='issue')
issue_router.register(r'comments', CommentViewset, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(issue_router.urls)),
]
