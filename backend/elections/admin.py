"""
"""
from django.contrib import admin
from elections.models import Election, Candidate


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    """
    """
    list_display = (
        'title',
        'election_event',
        'start_time',
        'end_time',
        'is_active'
    )


@admin.register(Candidate)
class ClassAdmin(admin.ModelAdmin):
    """
    """
    list_display =('first_name', 'last_name', 'election', 'user')