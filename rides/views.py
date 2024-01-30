from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from .models import RideModel
from .serializers import RideSearchSerializer, RideSerializer
from accounts.permissions import IsDriver
from rest_framework.permissions import AllowAny

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

class RideSearchView(GenericAPIView):
    serializer_class = RideSearchSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pickup_location = serializer.validated_data['pickup_location']
        destination_location = serializer.validated_data['destination_location']

        # Calculate distances and filter rides
        rides_within_3km = RideModel.objects.filter(
            departure_location__distance_lte=(pickup_location, 3000),
            destination_location__distance_lte=(destination_location, 3000)
        )

        rides_within_10km = RideModel.objects.filter(
            departure_location__distance_lte=(pickup_location, 10000),
            destination_location__distance_lte=(destination_location, 10000)
        )

        rides_more_than_10km = RideModel.objects.filter(
            departure_location__distance_gt=(pickup_location, 10000),
            destination_location__distance_gt=(destination_location, 10000)
        )

        # Serialize the queryset
        rides_within_3km_data = RideSerializer(rides_within_3km, many=True).data
        rides_within_10km_data = RideSerializer(rides_within_10km, many=True).data
        rides_more_than_10km_data = RideSerializer(rides_more_than_10km, many=True).data

        result = {
            'within_3km': rides_within_3km_data,
            'within_10km': rides_within_10km_data,
            'more_than_10km': rides_more_than_10km_data
        }

        return Response(result, status=status.HTTP_200_OK)