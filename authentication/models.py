from django.db import models
from django.utils import timezone

from accounts.models import UserProfile

class OTP(models.Model):
    OTP_TYPE_CHOICES = [
        ('email', 'Email OTP'),
        ('phone', 'Phone OTP'),
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    expiry_time = models.DateTimeField()
    otp_type = models.CharField(max_length=5, choices=OTP_TYPE_CHOICES)
    
    def has_expired(self):
        return self.expiry_time < timezone.now()

    def __str__(self):
        return f"OTP for {self.user}"

class ResetPasswordModel(models.Model):
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    expiry_time = models.DateTimeField()
    token = models.CharField(max_length=100)
    
    def has_expired(self):
        return self.expiry_time < timezone.now()

    def __str__(self):
        return f"{self.user}"
