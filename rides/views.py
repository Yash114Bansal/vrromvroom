from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from .models import RideModel
from .serializers import RideSerializer
from accounts.permissions import IsDriver

class RideViewSet(viewsets.ModelViewSet):
    """
    Create, Update, Delete Rides.
    
    API Endpoint For Drivers to Create, Read ,Update, Delete Rides. 
    """
    queryset = RideModel.objects.all()
    serializer_class = RideSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsDriver]

    def get_queryset(self):
            return RideModel.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if RideModel.objects.filter(user=user).exists():
            return Response({'error': 'You already have an active ride.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user != instance.user:
            return Response({'error': 'You do not have permission to delete this ride.'}, status=status.HTTP_403_FORBIDDEN)
        
        # TODO Inform All Users That ride has been canceled
        
        self.perform_destroy(instance)
        return Response({'message': 'Ride successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        # TODO  Inform All Users That ride has been Updated
        return super().update(request, *args, **kwargs)

