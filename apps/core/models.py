from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(_("name"), max_length=50, blank=False )
    address = models.CharField(_("address"), max_length=50, blank=False)

    def __str__(self):
        return f'{self.name}'


class EventManager(models.Manager):
    def get_future_events(self, when=timezone.now()):
        ''' Returns the queryset of all the events that are happening after <date> '''
        return super().get_queryset().filter(date__gte=when)

    def get_past_events(self, when=timezone.now()):
        ''' Returns the queryset of all the events that happened before <date> '''
        return super().get_queryset().filter(date__lte=when) 
    
class Event(models.Model):
    name = models.CharField(_("event name"), max_length=50)
    description = models.TextField(_("event description"), null=True)
    date = models.DateField(_("event date"), auto_now=False, auto_now_add=False)
    time = models.CharField(_("event time"), max_length=50)
    creator = models.ForeignKey(User, verbose_name=_("event creator"), on_delete=models.CASCADE, related_name='events_created')
    location = models.ForeignKey(Location, verbose_name=_("event location"), on_delete=models.CASCADE, related_name=_('events'))
    invited = models.ManyToManyField(User, verbose_name=_("invitees"), related_name='events_invited_to')
    attending = models.ManyToManyField(User, verbose_name=_("attendees"), related_name='events_attending')
    hosts = models.ManyToManyField(User, verbose_name=_("event hosts"), related_name='events_hosting')

    objects = EventManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['date']






