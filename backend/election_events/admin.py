"""
election_events/admin.py

Django admin configuration for the election_events application.
This module registers the ElectionEvent model with the Django admin interface.
"""
from django.contrib import admin
from election_events.models import ElectionEvent


@admin.register(ElectionEvent)
class ElectionEventAdmin(admin.ModelAdmin):
    """
    Django admin configuration for the ElectionEvent model.
    
    This class customizes how ElectionEvent objects are displayed and managed
    in the Django admin interface.
    
    Attributes:
        list_display (tuple): Fields to display in the admin list view
    """
    list_display = ('title', 'start_time', 'end_time', 'is_active')