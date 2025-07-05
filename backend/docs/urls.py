from django.urls import path
from . import views

app_name = 'docs'

urlpatterns = [
    path('', views.api_documentation, name='api-documentation'),
    path('schema/', views.api_schema, name='api-schema'),
]