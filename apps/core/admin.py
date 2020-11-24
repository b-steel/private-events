from django.contrib import admin
from .models import Location, Event, User

admin.register(Location)
admin.register(Event)
admin.register(User)