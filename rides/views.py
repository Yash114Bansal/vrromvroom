from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import RideModel
from .serializers import RideSerializer
from accounts.permissions import IsDriver

class RideCreateView(CreateAPIView):
    queryset = RideModel.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsDriver]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if RideModel.objects.filter(user=user).exists():
            return Response({'error': 'You already have an active ride.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)


class RideDeleteView(DestroyAPIView):
    queryset = RideModel.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsDriver]
    authentication_classes = [JWTAuthentication]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user != instance.user:
            return Response({'error': 'You do not have permission to delete this ride.'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({'message': 'Ride successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)

class MyRidesView(ListAPIView):
    queryset = RideModel.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return RideModel.objects.filter(user=user)
