from django.urls import path, include
from rest_framework import routers

from api.views import ProjectViewset


app_name = 'api'

router = routers.SimpleRouter()
router.register('project', ProjectViewset, basename='user')

urlpatterns = [
    path('', include(router.urls))
]
