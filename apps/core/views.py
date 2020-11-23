from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from . import models

class EventDetailView(LoginRequiredMixin, View):

    def get(self, request, id):
        event = get_object_or_404(models.Event, id=id)
        return render(request, 'core/event_details.html', {'event': event})

class EventIndexView(View):

    def get(self, request):
        future = models.Event.objects.get_future_events()
        past = models.Event.objects.get_past_events().order_by('-date')
    
        return render(request, 'core/index.html', {'past': past, 'future': future})