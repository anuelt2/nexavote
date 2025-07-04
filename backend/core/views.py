"""
"""
from django.views.generic import TemplateView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    """
    API Root View

    Welcome to NexaVote Electronic Voting Platform
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