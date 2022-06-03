from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserViewset


app_name = 'authentication'

router = routers.SimpleRouter()
router.register('user', UserViewset, basename='user')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='obtain_tokens'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('', include(router.urls))
]
