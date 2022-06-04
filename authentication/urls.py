from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserViewset


app_name = 'authentication'

router = routers.SimpleRouter()
router.register('users', UserViewset, basename='user')
router.register('signup', UserViewset, basename='signup')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('', include(router.urls)),
]
