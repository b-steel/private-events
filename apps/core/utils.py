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
            for i in invited:
                event.invited.add(i)
        if attending:
            for a in attending:
                event.attending.add(a)
        if host:
            for h in host:
                event.hosts.add(h)
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
        

def lorem_ipsum(n):
    ''' Make n users and n events.  Events are attended/hosted by a random assortment of users and are at random times in the future / past
    '''

    
    mf = ModelFactory()
    tu = mf.users.new(username='test_user', first_name='Test', last_name='User')
    for _ in range(n):
        u = mf.users.new()
        print(f'Created User {u.full_name}...')

    for _ in range(n):
        invited, hosts, attending = [], [], []
        users = list(User.objects.all())

        #invite random users
        invited.extend(random.sample(users, random.randint(0, n//3)))
        for user in invited:
            users.remove(user)
        #random users attend
        attending.extend(random.sample(users, random.randint(0, n//3)))
    
        #few random hosts from those attending
        for j in range(random.randint(0, min(3, len(attending)))):
            hosts.append(attending.pop())
        
        # Make the event
        e = mf.events.new(date=random.choice(['future', 'past']), invited=invited, attending=attending, host=hosts)
        print(f'Created Event {e.name}...')
