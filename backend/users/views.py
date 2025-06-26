"""
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers import RegisterViaTokenSerializer


class RegisterViaTokenView(APIView):
    """
    POST endpoint to register a voter via a one-time invitation token
    """
    def post(self, request):
        """
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
