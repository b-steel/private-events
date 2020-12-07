from django.test import TestCase, Client

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from django.core.cache import cache

from .models import Event, User
from .utils import ModelFactory

from bs4 import BeautifulSoup

class EventDetailsTestCase(TestCase):
    def setUp(self):

        self.mf = ModelFactory()
        self.c = Client()

        self.logged_in_user = self.mf.users.new()
        self.c.force_login(self.logged_in_user)


    def test_event_details_view(self):
        ''' Test for the detail view page of a single event'''

        self.attending_user = self.mf.users.new()
        self.invited_user = self.mf.users.new()
        self.host_user = self.mf.users.new()
        self.not_invited_user = self.mf.users.new()

        self.single_event = self.mf.events.new(attending=self.attending_user, invited=self.invited_user, host=self.host_user)
        
        response = self.c.get(reverse('core:event_details', kwargs={'event_id': self.single_event.pk}))

        with self.subTest('The correct details are displayed'):
            self.assertContains(response, f'{self.single_event.name}')
            self.assertContains(response, f'{self.single_event.location}')
            self.assertContains(response, f'{self.single_event.creator.first_name}')



class EventIndexTestCase(TestCase):
    def setUp(self):

        self.mf = ModelFactory()
        self.c = Client()

        self.logged_in_user = self.mf.users.new()
        self.c.force_login(self.logged_in_user)

    def test_index_view(self):
        ''' Test for index view of all events'''

        with self.subTest('Events are correctly listed in order, but with upcoming events before past events'):
            day1 = timezone.now() + timezone.timedelta(days=1)
            day2 = timezone.now() + timezone.timedelta(days=2)
            day3 = timezone.now() + timezone.timedelta(days=3)
            day4 = timezone.now() + timezone.timedelta(days=4)

            past1 = timezone.now() - timezone.timedelta(days=1)
            past2 = timezone.now() - timezone.timedelta(days=2)
            past3 = timezone.now() - timezone.timedelta(days=3)
            past4 = timezone.now() - timezone.timedelta(days=4)
            
            self.event1 = self.mf.events.new(date=day1)
            self.event2 = self.mf.events.new(date=day2)
            self.event3 = self.mf.events.new(date=day3)
            self.event4 = self.mf.events.new(date=day4)

            self.past_event1 = self.mf.events.new(date=past1)
            self.past_event2 = self.mf.events.new(date=past2)
            self.past_event3 = self.mf.events.new(date=past3)
            self.past_event4 = self.mf.events.new(date=past4)

            response = self.c.get(reverse('core:index'))

            page = response.content
            self.assertGreater(page.find(self.event2.name.encode('utf-8')),page.find(self.event1.name.encode('utf-8'))) #Event 2 should come after event 1
            self.assertGreater(page.find(self.event3.name.encode('utf-8')),page.find(self.event2.name.encode('utf-8')))
            self.assertGreater(page.find(self.event4.name.encode('utf-8')),page.find(self.event3.name.encode('utf-8')))
            # Past events
            self.assertGreater(page.find(self.past_event2.name.encode('utf-8')),page.find(self.past_event1.name.encode('utf-8')))
            self.assertGreater(page.find(self.past_event3.name.encode('utf-8')),page.find(self.past_event2.name.encode('utf-8')))
            self.assertGreater(page.find(self.past_event4.name.encode('utf-8')),page.find(self.past_event3.name.encode('utf-8')))


class CreateEventTestCase(TestCase):

    def setUp(self):
        self.mf = ModelFactory()
        self.c = Client()

        self.logged_in_user = self.mf.users.new()
        self.c.force_login(self.logged_in_user)


    def test_new_event(self):
        
        # Create some users to be listed as possible invitations
        other_users = []
        for i in range(4):
            other_users.append(self.mf.users.new(username=f'test_user-{i}'))
        
        response = self.c.get(reverse('core:create_event'))
        with self.subTest('The current user is not listed as an option for invitation'):
            self.assertNotContains(response, self.logged_in_user.full_name)

        with self.subTest('All other uses are listed as options for invitations'):
            for user in other_users:
                self.assertContains(response, user.full_name)
        
        # Details for an event to be created
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        ctx = {
            'name': 'Test Event',
            'date': tomorrow.strftime('%m/%d/%Y'),
            'location': 'a place', 
            'description': "It's gonna be so fun!",
        }
        # Make sure we populate the cache with some info on who's invited
        invite_data = {
            'invited': {
                other_users[1].pk: True, 
                other_users[0].pk: True, 
                other_users[2].pk: False,
            },
            'hosts': {
                other_users[3].pk: True
            }
        }
        cache.set('create_event', invite_data, 600)

        # Post the event data and get a response
        response = self.c.post(reverse('core:create_event'), ctx)
        
        event = Event.objects.last()

        with self.subTest('We get a redirect to the event page'):
            self.assertRedirects(response, reverse('core:event_details', args=[event.pk]))
        
        with self.subTest('The event has the correct details'):
            self.assertIn(other_users[0], event.invited.all())
            self.assertIn(other_users[1], event.invited.all())
            self.assertNotIn(other_users[2], event.invited.all())
            self.assertIn(other_users[3], event.hosts.all())
            self.assertEqual(self.logged_in_user, event.creator)

        with self.subTest('The cache has been cleared'):
            c = cache.get('create_event', 'no result')
            self.assertEqual(c, 'no result')
        

        resp = self.c.get(reverse('core:index'))
        with self.subTest('The event has been added to the index'):
            self.assertContains(resp, event.name)



        self.c.logout()
        self.c.force_login(other_users[0])
        resp = self.c.get(reverse('core:index'))
        with self.subTest('The invited users have an invitation notification'):
            self.assertContains(resp, 'You have 1 invite')