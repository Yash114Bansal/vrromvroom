from django.db import models
from accounts.models import UserProfile
from django.core.validators import FileExtensionValidator

class DocumentVerification(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='%(class)s_documents')
    document = models.FileField(upload_to='document_uploads/',validators=[
        FileExtensionValidator(['pdf','jpg', 'jpeg', 'png'])
    ])
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='verified_%(class)s')
    message = models.TextField(blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self._meta.verbose_name} for {self.user.name} || verified: {self.is_verified}'

class AadharCardModel(DocumentVerification):
    class Meta:
        verbose_name = 'Aadhar Card'

class DrivingLicenseModel(DocumentVerification):
    class Meta:
        verbose_name = 'Driving License'

class ImageWithVehicleModel(DocumentVerification):
    
    VEHICLE_TYPES = (
        ('2W', '2 Wheeler'),
        ('4W', '4 Wheeler'),
    )

    vehicle_type = models.CharField(max_length=2, choices=VEHICLE_TYPES, blank=True, null=True)
    plate_number = models.CharField(max_length=20, blank=True, null=True)
    vehicle_model = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        verbose_name = 'Image With Vehicle'
