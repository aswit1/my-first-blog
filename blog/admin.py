from django.contrib import admin
from .models import Post, PostComment, Direct_Message

# Register your models here.
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Direct_Message)