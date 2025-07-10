"""
core/views.py

This module defines the API root view that provides navigation links
to all available endpoints in the NexaVote Electronic Voting Platform.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse


UUID = "00000000-0000-0000-0000-000000000000"

@api_view(["GET"])
@permission_classes([AllowAny])     # temporary access to all API endpoints
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

        # API Root
        "api-root":         reverse("api-root", request=request, format=format),

        # API Documentation (Swagger / Redoc)
        "docs-swagger":         reverse("schema-swagger-ui", request=request, format=format),
        "docs-redoc":           reverse("schema-redoc", request=request, format=format),
        "docs-json":     reverse("schema-json", kwargs={"format": ".json"}, request=request),

        # Users
        "user-register":         reverse("users_api:register-via-token", request=request, format=format),
        "user-login":            reverse("users_api:login", request=request, format=format),
        "user-logout":           reverse("users_api:logout", request=request, format=format),
        "user-current-user":     reverse("users_api:current-user", request=request, format=format),
        "user-password-reset-confirm":     reverse("users_api:password-reset-confirm", request=request, format=format),
        "user-password-reset-request":     reverse("users_api:password-reset-request", request=request, format=format),
        
        # Invitations
        "invitation-create":    reverse("invitation-create", request=request, format=format),
        "invitation-list":      reverse("invitation-list", request=request, format=format),
        "invitation-detail":    reverse("invitation-detail", kwargs={"pk": UUID}, request=request, format=format),
        "invitation-by-event":  reverse("invitation-by-event", kwargs={"event_id": UUID}, request=request, format=format),
        "invitation-mark-used": reverse("invitation-mark-used", kwargs={"pk": UUID}, request=request, format=format),
        "invitation-by-token":  reverse("invitation-by-token", kwargs={"token": UUID}, request=request, format=format),
        "invitation-bulk-upload":    reverse("invitation-bulk-upload", request=request, format=format),

        # Election Events
        "event-events":     reverse("events_api:event-list", request=request, format=format),
        "event-detail":     reverse("events_api:event-detail", kwargs={"pk": UUID}, request=request, format=format),
        "event-my-event":   reverse("events_api:my-event", request=request, format=format),
        "event-create":     reverse("events_api:event-create", request=request, format=format),
        "event-update":     reverse("events_api:event-update", kwargs={"pk": UUID}, request=request, format=format),
        "event-delete":     reverse("events_api:event-delete", kwargs={"pk": UUID}, request=request, format=format),

        # Elections
        "election-create":    reverse("election-create", request=request, format=format),
        "election-list":      reverse("election-list", request=request, format=format),
        "election-detail":    reverse("election-detail", kwargs={"pk": UUID}, request=request, format=format),
        "election-update":    reverse("election-update", kwargs={"pk": UUID}, request=request, format=format),
        "election-delete":    reverse("election-delete", kwargs={"pk": UUID}, request=request, format=format),
        
        # Candidates
        "candidate-create":   reverse("candidate-create", request=request, format=format),
        "candidate-detail":   reverse("candidate-detail", kwargs={"pk": UUID}, request=request, format=format),
        "candidate-update":   reverse("candidate-update", kwargs={"pk": UUID}, request=request, format=format),
        "candidate-delete":   reverse("candidate-delete", kwargs={"pk": UUID}, request=request, format=format),
        "candidates-by-election":         reverse("candidates-by-election", kwargs={"election_id": UUID}, request=request, format=format),


        # Votes endpoints
        "vote-cast-vote":     reverse("votes:cast-vote", request=request, format=format),
        "vote-detail":        reverse("votes:vote-detail", kwargs={"pk": UUID}, request=request, format=format),
        "vote-my-votes":      reverse("votes:my-votes", request=request, format=format),
        "vote-verify-vote":   reverse("votes:verify-vote", request=request, format=format),
        "vote-check-status":  reverse("votes:check-vote-status", kwargs={"election_id": UUID}, request=request, format=format),
        
        # Vote Stats endpoints
        "vote-event-participation":  reverse("votes:event-participation", kwargs={"event_id": UUID}, request=request, format=format),
        "vote-elections-available":  reverse("votes:elections-available", request=request, format=format),
        "vote-election-results":     reverse("votes:election-results", kwargs={"election_id": UUID}, request=request, format=format),
        "vote-election-statistics":  reverse("votes:election-statistics", kwargs={"election_id": UUID}, request=request, format=format),
        "vote-audit-logs":           reverse("votes:audit-logs", request=request, format=format),
    })
