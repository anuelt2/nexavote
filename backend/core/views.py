"""
core/views.py

This module defines the API root view that provides navigation links
to all available endpoints in the NexaVote Electronic Voting Platform.
"""
from django.views.generic import TemplateView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    """
    API Root View for NexaVote Electronic Voting Platform.
    
    This view provides a centralized entry point that lists all available
    API endpoints organized by functionality. It serves as a navigation
    aid for API consumers.
    
    Args:
        request: The HTTP request object
        format: Optional format suffix for content negotiation
        
    Returns:
        Response: A dictionary containing URLs for all available API endpoints
        organized by category (Admin, Users, Invitations, Elections, etc.)
    """
    return Response({
        # Admin
        "admin":            reverse("admin:index", request=request, format=format),
        "api-root":         reverse("api-root", request=request, format=format),

        # Users
        "register":         reverse("register-via-token", request=request, format=format),
        
        # Invitations
        "invitations":      reverse("invitation-create", request=request, format=format),

        # Election Events
        "election-events":   reverse("election-event-list", request=request, format=format),

        # Elections (public)
        "elections" :        reverse("election-list", request=request, format=format),
        "candidates":        reverse("candidate-list", request=request, format=format),

        # Votes endpoints
        "cast-vote":         reverse("votes:cast-vote", request=request, format=format),
        "my-votes":          reverse("votes:my-votes", request=request, format=format),
        "verify-vote":       reverse("votes:verify-vote", request=request, format=format),
        "audit-logs":        reverse("votes:audit-logs", request=request, format=format),

        # Elections (admin)
        "election-admin-create":    reverse("election-admin-create", request=request, format=format),
        "candidate-admin_create":   reverse("candidate-admin-create", request=request, format=format),
        "election-admin-detail":    "<use /elections/admin/<uuid>/>",
        "candidate-admin-detail":   "<use /candidates/admin/<uuid>/>",
    })


class HomeView(TemplateView):
    """
    """
    template_name = "home.html"
