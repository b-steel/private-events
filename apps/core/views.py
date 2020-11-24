from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from . import models, forms
from .models import User

class EventDetailView(LoginRequiredMixin, View):

    def get(self, request, event_id):
        event = get_object_or_404(models.Event, id=event_id)
        return render(request, 'core/event_details.html', {'event': event})

class EventIndexView(View):

    def get(self, request):
        future = models.Event.objects.get_future_events()
        past = models.Event.objects.get_past_events().order_by('-date')
    
        return render(request, 'core/index.html', {'past': past, 'future': future})

class CreateEventView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.EventForm()
        return render(request, 'core/create_event.html', {'form': form, 'user_list': User.objects.all().exclude(username=request.user.username)})

    def post(self, request):
        bound_form = forms.EventForm(request.POST)
        if bound_form.is_valid():
            event = models.Event.objects.create(
                name=bound_form.cleaned_data['name'], 
                description=bound_form.cleaned_data['description'],
                date=bound_form.cleaned_data['date'],
                creator=request.user
            )
            return render(request, 'core/stage_2.html', {'event': event})
        else:
            return render(request, 'core/create_event.html', {'form': bound_form})

class EditEventView(LoginRequiredMixin, View):
    def validate_host(self, person:User, event:models.Event)-> bool:
        if person in event.objects.hosts.all():
            return True
        return False

    def get(self, request, event_id):
        event = get_object_or_404(models.Event, id=event_id)
        if self.validate_host(request.user, event):
            form = forms.EventForm(event)
            return render(request, 'core/edit_event.html', {'form': form})
        else:
            return redirect(reverse('accounts:login'))

    def post(self, request, event_id):
        form = forms.EventForm(request.POST)
        event = get_object_or_404(models.Event, id=event_id)
        
        if form.is_valid():
            event.name = form.cleaned_data['name']
            event.desription = form.cleaned_data['description']
            event.date = form.cleaned_data['date']
            event.save()

            return render(request, 'core/event_details', {'event': event})
        else: 
            return render(request, 'core/edit_event.html', {'form': form})