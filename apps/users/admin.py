from django.contrib import admin

from .models import User, UserFollow

admin.site.register(User)
admin.site.register(UserFollow)
