from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from .models import RideModel
from .serializers import RideSearchSerializer, RideSerializer, RideViewSerializer
from accounts.permissions import IsDriver
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import F

from django.contrib.gis.geos import GEOSGeometry
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
    

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "departure_offset",
                openapi.IN_QUERY,
                description="",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "destination_offset",
                openapi.IN_QUERY,
                description="",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "departure_time_start",
                openapi.IN_QUERY,
                description="",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "departure_time_end",
                openapi.IN_QUERY,
                description="",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pickup_location = serializer.validated_data['pickup_location']
        destination_location = serializer.validated_data['destination_location']

        # Get departure and destination offset distances from query parameters
        departure_offset = request.query_params.get('departure_offset')
        destination_offset = request.query_params.get('destination_offset')

        # Get departure datetime range from query parameters
        departure_time_start = request.query_params.get('departure_time_start')
        departure_time_end = request.query_params.get('departure_time_end')

        # Apply filters only if offset distances are provided
        rides_within_offset = RideModel.objects.all()
        if departure_offset:
            rides_within_offset = rides_within_offset.filter(
                departure_location__distance_lte=(pickup_location, departure_offset)
            )
        if destination_offset:
            rides_within_offset = rides_within_offset.filter(
                destination_location__distance_lte=(destination_location, destination_offset)
            )

        # Apply departure datetime range filter if both start and end are provided
        if departure_time_start and departure_time_end:
            rides_within_offset = rides_within_offset.filter(
                departure_time__range=(departure_time_start, departure_time_end)
            )

        # Serialize the queryset
        # rides_within_offset_data = RideSerializer(rides_within_offset, many=True).data
        rides_within_offset = rides_within_offset.annotate(
            departure_distance=Distance('departure_location', GEOSGeometry(pickup_location,srid=4326)),
            destination_distance=Distance('destination_location', GEOSGeometry(destination_location,srid=4326)),
        )

        # Serialize the queryset with distances using RideViewSerializer
        rides_within_offset_data = RideViewSerializer(rides_within_offset, many=True).data

        return Response({'within_offset': rides_within_offset_data}, status=status.HTTP_200_OK)

        # return Response(rides_within_offset_data, status=status.HTTP_200_OK)