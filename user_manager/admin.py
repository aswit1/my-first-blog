from django.contrib import admin
from .models import UserProfile, Weather
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Weather)