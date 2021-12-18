from django.contrib import admin
from .models import Review, Ticket, UserFollow


admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollow)
