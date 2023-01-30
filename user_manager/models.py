from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=25)
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    text_updates = models.BooleanField(default=True)
    email_updates = models.BooleanField(default=True)
    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        return name + ' user profile'

class Weather(models.Model):
    temp = models.FloatField(blank=True, null=True)