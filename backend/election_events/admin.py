"""
"""
from django.contrib import admin
from election_events.models import ElectionEvent


@admin.register(ElectionEvent)
class ElectionEventAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('title', 'start_time', 'end_time', 'is_active')