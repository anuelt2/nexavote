"""
users/permissions.py

Custom permission classes for the voting system.
"""
from rest_framework import permissions
from .models import VoterProfile


class IsVoter(permissions.BasePermission):
    """
    Permission class to check if user is a voter.
    Only allows access to users who have a VoterProfile.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has a voter profile.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user has a VoterProfile
        try:
            VoterProfile.objects.get(user=request.user)
            return True
        except VoterProfile.DoesNotExist:
            return False


class IsElectionAdmin(permissions.BasePermission):
    """
    Permission class to check if user is an election administrator.
    Allows access to staff users or users in the 'ElectionAdmins' group.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated and is an election admin.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user is staff or superuser
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Check if user has admin role
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return True
        
        # Check if user is in ElectionAdmins group
        return request.user.groups.filter(name='ElectionAdmins').exists()


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class to allow access to owners of objects or admins.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user owns the object or is an admin.
        """
        # Allow access to admins
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return True
        
        # Check if user is in ElectionAdmins group
        if request.user.groups.filter(name='ElectionAdmins').exists():
            return True
        
        # Check if user owns the object
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'voter') and hasattr(obj.voter, 'user'):
            return obj.voter.user == request.user
        
        return False


class IsVoterOrAdmin(permissions.BasePermission):
    """
    Permission class that allows access to voters or admins.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated and is either a voter or admin.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user is admin
        if (request.user.is_staff or 
            request.user.is_superuser or 
            (hasattr(request.user, 'role') and request.user.role == 'admin') or
            request.user.groups.filter(name='ElectionAdmins').exists()):
            return True
        
        # Check if user is a voter
        try:
            VoterProfile.objects.get(user=request.user)
            return True
        except VoterProfile.DoesNotExist:
            return False