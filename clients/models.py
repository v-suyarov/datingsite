from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('M', ' Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="participant", )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to='avatars/')
    email = models.EmailField(unique=True)
    likes = models.ManyToManyField('self', related_name='liked_by', symmetrical=False, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
