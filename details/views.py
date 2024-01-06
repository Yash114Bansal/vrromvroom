from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserDetailsSerializer

class UserDetailsView(RetrieveAPIView):
    """
    Get User Details.

    API Endpoint To Fetch User Details
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsSerializer

    def get_object(self):
        return self.request.user