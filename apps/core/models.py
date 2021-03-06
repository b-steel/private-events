from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth.models import User as auth_user
from django.core.cache import cache
from django.core.exceptions import ValidationError

class User(auth_user):
    @property
    def full_name(self):
        return self.first_name.capitalize() + ' ' + self.last_name.capitalize()

    def attend_event(self, event):
        if self in event.invited.all():
            event.invited.remove(self)
            event.attending.add(self)
            return True
        return False
    

class EventManager(models.Manager):
    def get_future_events(self, when=timezone.now()):
        ''' Returns the queryset of all the events that are happening after <date> '''
        return super().get_queryset().filter(date__gte=when)

    def get_past_events(self, when=timezone.now()):
        ''' Returns the queryset of all the events that happened before <date> '''
        return super().get_queryset().filter(date__lte=when) 

def validate_not_past(date):
    if date < timezone.now().date():
        raise ValidationError(
            _(f'{date} is in the past, only future dates are allowed'),
            code='past_date')


class Event(models.Model):
    name = models.CharField(_("event name"), max_length=50)
    description = models.TextField(_("event description"), null=True)
    date = models.DateField(_("event date"), auto_now=False, auto_now_add=False, validators=[validate_not_past])
    time = models.CharField(_("event time"), max_length=50)
    creator = models.ForeignKey(User, verbose_name=_("event creator"), on_delete=models.CASCADE, related_name='events_created')
    location = models.CharField(_("event location"), max_length=100)
    invited = models.ManyToManyField(User, verbose_name=_("invitees"), related_name='events_invited_to')
    attending = models.ManyToManyField(User, verbose_name=_("attendees"), related_name='events_attending')
    hosts = models.ManyToManyField(User, verbose_name=_("event hosts"), related_name='events_hosting')

    objects = EventManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['date']

    def hosts_are_not_attending(self):
        ''' If someone is both made a host and invited, remove them from the invited list. Host supercedes invites'''
        hosts = self.hosts.all()
        invited = self.invited.all()
        for person in hosts:
            if person in invited:
                self.invited.remove(person)



