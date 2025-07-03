"""
"""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import (
    RegisterViaTokenView,
    RegisterViaTokenHTMLView,
    LogoutAnyMethodView,
    AdminStaffRegistrationView,
)


urlpatterns = [
    # API routes
    path('register/voter/', RegisterViaTokenView.as_view(), name='register-via-token'),
    # path('register/admin-staff/', AdminStaffRegistrationView.as_view(), name='register-admin-staff'),

    # HTML templates routes
    path('register/voter/html/', RegisterViaTokenHTMLView.as_view(), name='register-voter-html'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutAnyMethodView.as_view(), name='html-logout'),
]