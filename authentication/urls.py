from django.urls import path
from authentication.views import UserAPIView


app_name = 'authentication'

urlpatterns = [
    path('user/', UserAPIView.as_view())
]
