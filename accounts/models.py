from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator
from .managers import UserManager

class AKGECEmailValidator(RegexValidator):
    regex = r'^[^@]+@akgec\.ac\.in$'
    message = 'Only @akgec.ac.in email addresses are allowed.' 

class PhoneNumberValidator(RegexValidator):
    regex = r'^\+?1?\d{9,15}$'
    message = 'Phone Number must be entered in correct format.'

class UserProfile(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, primary_key=True,validators= [AKGECEmailValidator()])
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True,validators=[PhoneNumberValidator])

    profile_picture = models.ImageField(
        upload_to="profiles/", default=None, blank=True
    )

    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    verified_driver = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='user_profiles')
    user_permissions = models.ManyToManyField(Permission, related_name='user_profiles')

    objects = UserManager()
