from django.contrib.gis.db import models
from accounts.models import UserProfile

class RideModel(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('onway', 'On Way'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    seat_available = models.IntegerField()
    departure_location = models.PointField()
    destination_location = models.PointField()
    departure_time = models.DateTimeField()
    fare = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    passengers = models.ManyToManyField(UserProfile, related_name='rides_as_passenger', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming', null=True)

    def __str__(self):
        return f'Ride {self.id} by {self.user} - {self.get_status_display()}'
