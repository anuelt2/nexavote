"""
"""
from django.urls import path
from users.views import RegisterViaTokenView


urlpatterns = [
        path(
            'register/',
            RegisterViaTokenView.as_view(),
            name='register-via-token'
            ),
        ]
