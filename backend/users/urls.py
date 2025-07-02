"""
"""
from django.urls import path
from users.views import RegisterViaTokenView


urlpatterns = [
    path(
        'register/voter/',
        RegisterViaTokenView.as_view(),
        name='register-via-token'
    ),

     path(
        'register/admin-staff/',
        AdminStaffRegistrationView.as_view(),
        name='register-admin-staff'
    ),
]