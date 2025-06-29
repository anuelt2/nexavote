"""
Votes model for the /vote endpoint
"""
from django.urls import path
from users.views import RegisterViaTokenView


urlpatterns = [
    path(
        'vote/',
        Vote.as_view(),
        name='vote'
    ),
]