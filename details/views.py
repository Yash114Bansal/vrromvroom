from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserDetailsSerializer, UserDetailsUpdateSerializer

class UserDetailsView(RetrieveUpdateAPIView):
    """
    Get or Update User Details.

    API Endpoint To Fetch or Update User Details
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailsSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserDetailsUpdateSerializer
