from django.contrib import admin

from .models import Review, Ticket

admin.site.register(Ticket)
admin.site.register(Review)
