from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.cache import cache

from . import models, forms
from .models import User

import json
class AboutView(View):
    def get(self, request):
        return render(request, 'core/about.html', {})

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
        # exclude the creator
        user_list = User.objects.all().exclude(username=request.user.username)
        return render(request, 'core/create_event.html', {'form': form, 'user_list': user_list})

    def post(self, request):
        bound_form = forms.EventForm(request.POST)
        if bound_form.is_valid():
            creator = User.objects.get(username=request.user.username)
            event = models.Event.objects.create(
                name=bound_form.cleaned_data['name'],
                description=bound_form.cleaned_data['description'],
                date=bound_form.cleaned_data['date'],
                creator=creator
            )
            # Cached invitation / host data   
            data = cache.get('create_event', None)
            if data:
                for item in data['invited'].items():
                    if item[1]: #if true means the user is invited
                        event.invited.add(User.objects.get(id=item[0]))
                for item in data['hosts'].items():
                    if item[1]: #if true means the user is host
                        event.hosts.add(User.objects.get(id=item[0]))
            event.hosts_are_not_attending()
            event.save()
            # Delete cached data so future events don't duplicate it 
            cache.delete('create_event')

            return redirect(reverse('core:event_details', args=[event.id]))

        else:
            return render(request, 'core/create_event.html', {'form': bound_form})


class EditEventView(LoginRequiredMixin, View):
    def validate_host(self, person: User, event: models.Event) -> bool:
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

# AJAX views
def ajax_invite_users(request):
    '''It's a GET request'''
    data = json.loads(request.GET['data'])
    cache.set('create_event', data, 600)
    return JsonResponse(data)

def ajax_accept_invite(request):
    event_id = request.GET['event_id']
    event_id = int(event_id)
    event = models.Event.objects.get(pk=event_id)
    user = User.objects.get(username=request.user.username)
    event.invited.remove(user)
    event.attending.add(user)
    event.save()
    return HttpResponse('Success')


