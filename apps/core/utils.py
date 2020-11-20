from .models import Event, Location
import random
from django.contrib.auth.models import User
from django.utils import timezone
from essential_generators import DocumentGenerator

NOTHING = object()

class UserFactory():
    def __init__(self):
        michelle = {
            'first_name': 'Michelle', 
            'last_name': 'Obama',
            'email': 'michelle@wh.gov', 
            'username': 'firstLady',
            'password': 'michellepass'
        }
        barack = {
            'first_name': 'Barack', 
            'last_name': 'Obama',
            'email': 'barack@wh.gov', 
            'username': '44thPREZ',
            'password': 'barackpass'
        }
        aoc = {
            'first_name': 'Alexandria', 
            'last_name': 'Ocasio-ortrez',
            'email': 'alexandria@congress.gov', 
            'username': 'AOC',
            'password': 'alexandriapass'
        }
        self.michelle = User.objects.get_or_create(**michelle)[0]
        self.barack = User.objects.get_or_create(**barack)[0]
        self.aoc = User.objects.get_or_create(**aoc)[0]

    @property
    def one(self):
        return self.michelle

    @property
    def two(self):
        return self.barack

    @property
    def three(self):
        return self.aoc

    def random(self):
        return random.choice([self.michelle, self.barack, self.aoc])

           
class LocationFactory():
    def __init__(self):
        white_house = {
            'name': 'The Whitehouse', 
            'address': '100 Capitol Dr, Washington DC'
        }
        the_hill = {
            'name': 'The Hill', 
            'address': 'around the corner from The Whitehouse'
        }
        van = {
            'name': 'A Van',
            'address': 'Down by the River'
        }
        self.white_house = Location.objects.get_or_create(**white_house)[0]
        self.the_hill = Location.objects.get_or_create(**the_hill)[0]
        self.van = Location.objects.get_or_create(**van)[0]
    
    @property
    def one(self):
        return self.white_house

    @property
    def two(self):
        return self.the_hill

    @property
    def three(self):
        return self.van

    def random(self):
        return random.choice([self.white_house, self.the_hill, self.van])


class EventFactory():
    def __init__(self):
        self.users = UserFactory()
        self.locations = LocationFactory()
        self.gen = DocumentGenerator()
        self.last = None
        self.events = []
    

    def new(self, creator=NOTHING, location=NOTHING, name=NOTHING, description=NOTHING, invited=NOTHING, attending=NOTHING, date=NOTHING):
        user_list = [self.users.one, self.users.two, self.users.three]

        if creator is NOTHING:
            creator = self.users.random()
        if location is NOTHING:
            location = self.locations.random()
        if name is NOTHING:
            name = self.gen.name().capitalize()
        if description is NOTHING:
            description = self.gen.sentence()
        if invited is NOTHING:
            invited = user_list.pop(random.randint(0, len(user_list) - 1))
        if attending is NOTHING:
            attending = user_list.pop(random.randint(0, len(user_list) - 1))
        
        if date == 'future':
            date = timezone.now() + timezone.timedelta(days=random.randint(2, 100))
        elif date == 'past':
            date = timezone.now() - timezone.timedelta(days=random.randint(2, 100))
        elif date is NOTHING:
            date = timezone.now() + timezone.timedelta(days=1)

        event = Event.objects.create(name=name, creator=creator, date=date, time=date, description=description, location=location)
        event.invited.add(invited)
        event.attending.add(attending)
        event.save()

        self.events.append(event)
        self.last=event
        self.__setattr__(event.name, event)
        return event
        
class ModelFactory():
    def __init__(self):
        self.user = UserFactory()
        self.location = LocationFactory()
        self.event = EventFactory()
        