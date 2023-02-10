from django.contrib import admin
from .models import Poll, Pollv2, PollQ

# Register your models here.
admin.site.register(Poll)
admin.site.register(Pollv2)
admin.site.register(PollQ)