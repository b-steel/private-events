from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Location, Event
from .utils import ModelFactory



class LocationTestCase(TestCase):

    def test_attributes(self):
        '''A location must have a name and an address'''
        no_addy = Location.objects.create(name='no address')
        no_name = Location.objects.create(address='no name')
        good_location = Location.objects.create(name='good', address='here')

        self.assertRaises(ValidationError, no_addy.full_clean)
        self.assertRaises(ValidationError, no_name.full_clean)

        

class EventTestCase(TestCase):
    def setUp(self):

        self.mf = ModelFactory()
        self.c = Client()

        self.logged_in_user = self.mf.users.new()
        self.c.force_login(self.logged_in_user)

        self.test_location = self.mf.locations.new()


    def test_creator_related_name(self):
        self.event_with_logged_in_creator = self.mf.events.new(creator=self.logged_in_user)
        self.assertIn(self.event_with_logged_in_creator, self.logged_in_user.events_created.all())

    
    def test_location_related_name(self):
        self.event_at_test_location = self.mf.events.new(location=self.test_location)
        self.assertIn(self.event_at_test_location, self.test_location.events.all())
        self.assertNotIn(self.event_with_logged_in_creator, self.test_location.events.all())

    def test_invited(self):
        self.invited_user = self.mf.users.new()
        self.event_with_invited_users = self.mf.events.new(invited=self.invited_user)


        with self.subTest('a person is in the events invited list'):
            self.assertIn(self.invited_user, self.event_with_invited_users.invited.all())
        with self.subTest('An event is in the persons invited to list'):
            self.assertIn(self.event_with_invited_users, self.invited_user.events_invited_to.all())
 