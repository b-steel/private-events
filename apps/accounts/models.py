from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone

class User(models.Model):
    username = models.CharField(_("username"), max_length=50, unique=True)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    email = models.EmailField(_("email"), max_length=254)
    created_at = models.DateField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    
class Location(models.Model):
    name = models.CharField(_("name"), max_length=50)
    address = models.CharField(_("address"), max_length=50)
    
class Event(models.Model):
    date = models.DateField(_("event date"), auto_now=False, auto_now_add=False)
    time = models.TimeField(_("event time"), auto_now=False, auto_now_add=False)
    location = models.ForeignKey(Location, verbose_name=_("event location"), on_delete=models.CASCADE, related_name=_('events'))
    invited = models.ManyToManyField("accounts.User", verbose_name=_("invitees"), related_name='events_invited_to')
    attending = models.ManyToManyField("accounts.User", verbose_name=_("attendees"), related_name='events_attending')
    creator = models.ForeignKey("accounts.User", verbose_name=_("event creator"), on_delete=models.CASCADE, related_name='events_created')
    hosts = models.ManyToManyField("accounts.User", verbose_name=_("event hosts"), related_name='events_hosting')
    description = models.TextField(_("event description"))


