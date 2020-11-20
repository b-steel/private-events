from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(_("name"), max_length=50, blank=False )
    address = models.CharField(_("address"), max_length=50, blank=False)

    def __str__(self):
        return f'{self.name}'


    
class Event(models.Model):
    name = models.CharField(_("event name"), max_length=50)
    
    description = models.TextField(_("event description"), null=True)
    
    date = models.DateField(_("event date"), auto_now=False, auto_now_add=False)

    time = models.TimeField(_("event time"), auto_now=False, auto_now_add=False)
    
    creator = models.ForeignKey(User, verbose_name=_("event creator"), on_delete=models.CASCADE, related_name='events_created')
    
    location = models.ForeignKey(Location, verbose_name=_("event location"), on_delete=models.CASCADE, related_name=_('events'))
    
    invited = models.ManyToManyField(User, verbose_name=_("invitees"), related_name='events_invited_to')
    
    attending = models.ManyToManyField(User, verbose_name=_("attendees"), related_name='events_attending')
    
    hosts = models.ManyToManyField(User, verbose_name=_("event hosts"), related_name='events_hosting')

    def __str__(self):
        return f'{self.name}'




def create_sample_models():

    # Users
    allison = User(first_name='Allison', last_name='Hyatt', email='allison@email.com', username='a-dawg')
    allison.save()
    ben = User.objects.create(username='bean', email='b@email.com', first_name='Ben', last_name='Hidden')
    
    # Locations
    casa = Location.objects.create(name='Mi Casa', address='Tortilla Flat')
    park = Location.objects.create(name='The Park', address='100 Road St')

    # Events
    picnic = Event.objects.create(
        date=timezone.datetime(year=2020, month=12, day=1),
        time=timezone.datetime(year=2020, month=12, day=1),
        location=park,
        creator=allison,
        name='Picnic at the park',
    )
    big_party = Event.objects.create(
        date=timezone.datetime(year=2020, month=12, day=4),
        time=timezone.datetime(year=2020, month=12, day=4),
        location=casa,
        creator=allison,
        name='Bigass Party at my House',
        description='We\'re gonna rage our faces off'
    )