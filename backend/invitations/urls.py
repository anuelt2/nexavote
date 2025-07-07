"""
"""
from django.urls import path
from invitations.views import InvitationCreateAPIView, InvitationCreateView
from . import views


app_name = 'invitations'

urlpatterns =[
    path('create/', InvitationCreateAPIView.as_view(), name='invitation-create'),
    path('invite/', InvitationCreateView.as_view(), name='invite-voter'),

     # CSV upload
    path('upload-csv/<uuid:event_id>/', views.CSVUploadView.as_view(), name='csv-upload'),
    path('csv-results/<uuid:event_id>/', views.CSVResultsView.as_view(), name='csv-results'),
    
    # API endpoint
    path('api/upload-csv/<uuid:event_id>/', views.CSVUploadAPIView.as_view(), name='api-csv-upload'),
]