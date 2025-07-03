"""
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from users.serializers import RegisterViaTokenSerializer, AdminStaffRegistrationSerializer


class RegisterViaTokenView(APIView):
    """
    POST endpoint to register a voter via a one-time invitation token
    """
    def post(self, request):
        """
        Process voter registration via invitation token.
        
        Args:
            request (Request): The HTTP request object
        
        Returns:
            Response: Registration success or error response
        """
        serializer = RegisterViaTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                    {"message": "Voter registration successful"},
                    status=status.HTTP_201_CREATED
                    )
        return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )


class AdminStaffRegistrationView(APIView):
    """
    View to handle direct registration for admin and staff users.
    
    This view allows administrators to create admin and staff accounts
    without using an invitation token.
    """
    permission_classes = [permissions.IsAdminUser]  # Only admins can create admin/staff accounts

    def post(self, request):
        """
        Process admin or staff user registration.
        
        Args:
            request (Request): The HTTP request object
        
        Returns:
            Response: Registration success or error response
        """
        serializer = AdminStaffRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Admin/Staff registration successful"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )                