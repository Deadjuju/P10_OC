from django.urls import path, include
from rest_framework_nested import routers

from api.views import ProjectViewset, ContributorViewset


app_name = 'api'

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewset, basename='projects')

project_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
project_router.register(r'users', ContributorViewset, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(project_router.urls)),
]

# ENDPOINT / projects / <project_id> / users
