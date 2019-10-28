from django.contrib import admin
from .models import User, User_like_topic, User_like_comment

admin.site.register(User)
admin.site.register(User_like_topic)
admin.site.register(User_like_comment)
# Register your models here.
