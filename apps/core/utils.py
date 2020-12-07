from .models import Event, User
import random
from django.utils import timezone
from essential_generators import DocumentGenerator

NOTHING = object()
gen = DocumentGenerator()

class UserFactory():
    def __init__(self):
        self.last = None

    def new(self, username=NOTHING, first_name=NOTHING, last_name=NOTHING, password=NOTHING, email=NOTHING):
        if username is NOTHING:
            username = '_'.join(gen.name().lower().split(' '))
        if first_name is NOTHING:
            first_name = username.split('_')[0].capitalize()
        if last_name is NOTHING:
            last_name = username.split('_')[1].capitalize()
        if password is NOTHING:
            password = gen.slug()
        if email is NOTHING:
            email = gen.email()

        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        self.last = user
        self.__setattr__(user.username, user)
        return user

    @property
    def all(self):
        return list(User.objects.all())

    def random(self):
        if self.all:
            return random.choice(self.all) 
        else: 
            return self.new()


class StringLocationFactory():
    def new(self):
        return f"{random.randrange(1000, 10000)} {gen.name().split(' ')[1]} {random.choice(['St', 'Rd', 'Ln', 'Ave'])}"

class EventFactory():
    def __init__(self):
        self.users = UserFactory()
        self.locations = StringLocationFactory()
        self.last = None
    

    def new(self, creator=NOTHING, location=NOTHING, name=NOTHING, description=NOTHING, invited=NOTHING, attending=NOTHING, date=NOTHING, host=NOTHING):

        if creator is NOTHING:
            creator = self.users.new()
        if location is NOTHING:
            location = self.locations.new()
        if name is NOTHING:
            name = gen.name().capitalize()
        if description is NOTHING:
            description = gen.sentence()
        if invited is NOTHING:
            invited = []
        if attending is NOTHING:
            attending = []
        if host is NOTHING: 
            host = []
        
        if date == 'future':
            date = timezone.now() + timezone.timedelta(days=random.randint(2, 100))
        elif date == 'past':
            date = timezone.now() - timezone.timedelta(days=random.randint(2, 100))
        elif date is NOTHING:
            date = timezone.now() + timezone.timedelta(days=1)

        event = Event.objects.create(name=name, creator=creator, date=date, description=description, location=location)

        if invited:
            event.invited.add(invited)
        if attending:
            event.attending.add(attending)
        if host:
            event.hosts.add(host)
        event.save()

        self.last=event
        self.__setattr__(event.name, event)
        return event

    @property
    def all(self):
        return list(Event.objects.all())

    def random(self):
        if self.all:
            return random.choice(self.all) 
        else: 
            return self.new()



class ModelFactory():
    def __init__(self):
        self.users = UserFactory()
        self.locations = StringLocationFactory()
        self.events = EventFactory()
        