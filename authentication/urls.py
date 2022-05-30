from django.urls import path, include
from rest_framework import routers

from authentication.views import UserViewset


app_name = 'authentication'

router = routers.SimpleRouter()
router.register('user', UserViewset, basename='user')

urlpatterns = [
    path('', include(router.urls))
]
