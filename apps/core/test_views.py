from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse

from .models import Location, Event, User
from .utils import ModelFactory

from bs4 import BeautifulSoup

class EventTestCase(TestCase):
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
        
        response = self.c.get(f'/event/{self.single_event.id}/')

        # TESTS FOR LOGGED IN USERS
        with self.subTest('The correct details are displayed'):
            self.assertContains(response, f'{self.single_event.name}')
            self.assertContains(response, f'{self.single_event.location}')
            self.assertContains(response, f'{self.single_event.creator.first_name}')
            # self.assertContains(response, f'{self.single_event.date.FORMAT}')  Need to format

        with self.subTest('An event lists those attending, but not those invited'):
            self.assertNotContains(response, f'{self.invited_user.username}') # invited, not attending
            self.assertContains(response, f'{self.attending_user.username}') # attending
        
        
        # TESTS FOR INVITED USERS
        with self.subTest('An invited user has an "Attend" option'):
            self.c.logout()
            self.c.force_login(self.invited_user)
            response = self.c.get(f'/event/{self.single_event.id}/')
            self.assertContains(response, 'Attend')

        # TESTS FOR NON-INVITED USERS
        with self.subTest('A non-invited user does not have an option to attend'):
            self.c.logout()
            self.c.force_login(self.not_invited_user)
            response = self.c.get(f'/event/{self.single_event.id}/')
            self.assertNotContains(response, 'Attend')

        # TESTS FOR ATTENDING USERS
        with self.subTest('An attending user has the option of un-RSVPing'):
            self.c.logout()
            self.c.force_login(self.attending_user)
            response = self.c.get(f'/event/{self.single_event.id}/')
            self.assertContains(response, "Don't Attend")

        # TESTS FOR THE HOST OF AN EVENT
        with self.subTest('A host has the option of editing the event details'):
            self.c.logout()
            self.c.force_login(self.host_user)
            response = self.c.get(f'/event/{self.single_event.id}/')
            
            self.assertContains(response, 'Edit Details')
            edit_url = reverse("core:edit_event", args=[self.single_event.id])
            self.assertContains(response, f'href="{edit_url}"')


        # TESTS FOR LOGGED OUT USERS
        with self.subTest('A logged out user cannot see details'):
            self.c.logout()
            response = self.c.get(f'/event/{self.single_event.id}/')
            #should redirect to login
            self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('core:event_details', kwargs={'event': self.single_event.pk})}")

class EventIndexTestCase(TestCase):
    def setUp(self):

        self.mf = ModelFactory()
        self.c = Client()

        self.logged_in_user = self.mf.users.new()
        self.c.force_login(self.logged_in_user)

    def test_event_index_view(self):
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

            response = self.c.get(reverse('core:event_index'))

            page = response.content
            self.assertGreater(page.find(self.event2.name.encode('utf-8')),page.find(self.event1.name.encode('utf-8'))) #Event 2 should come after event 1
            self.assertGreater(page.find(self.event3.name.encode('utf-8')),page.find(self.event2.name.encode('utf-8')))
            self.assertGreater(page.find(self.event4.name.encode('utf-8')),page.find(self.event3.name.encode('utf-8')))
            # Past events
            self.assertGreater(page.find(self.past_event2.name.encode('utf-8')),page.find(self.past_event1.name.encode('utf-8')))
            self.assertGreater(page.find(self.past_event3.name.encode('utf-8')),page.find(self.past_event2.name.encode('utf-8')))
            self.assertGreater(page.find(self.past_event4.name.encode('utf-8')),page.find(self.past_event3.name.encode('utf-8')))

        # with self.subTest('All events have a link to their own detail page'):
        #     events = [
        #         self.event1, self.event2, self.event3, self.event4, self.past_event1, self.past_event2, self.past_event3, self.past_event4, 
        #     ]
        #     soup = BeautifulSoup(response.content, 'html.parser')
            # Need to implement once we know what the html will look like


class CreateEventTestCase(TestCase):

    def setUp(self):
        self.mf = ModelFactory()
        self.c = Client()

        self.logged_in_user = self.mf.users.new()
        self.c.force_login(self.logged_in_user)


    def test_submit_form(self):
        
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        ctx = {
            'name': 'Test Event',
            'date': tomorrow, 
            'time': tomorrow, 
            'location': 'a place', 
            'description': "It's gonna be so fun!",
        }
        response = self.c.post(reverse('core:create_event'), **ctx)
        new_event = Event.objects.filter(name=ctx['name']).filter(date=tomorrow)[0]
        
        with self.subTest('A valid event submits to stage 2'):
            self.assertNotEqual(new_event, None)
            self.assertRedirects(response, reverse('core:event_stage_two', args=[new_event.id]))


        response = self.c.get(reverse('core:event_stage_two', args=[new_event.id]))
        
        with self.subTest('Stage 2 page links to the event details'):
            self.assertContains(response, reverse('core:event_details', args=[new_event.id]))

        with self.subTest('Self is not listed as option for host or invited'):
            invite_response = self.c.get(reverse('core:get_potential_invites'))
            self.assertFalse(new_event.creator.username in invite_response['users_to_invite'])

        # with self.subTest('A location thats not in the database'):
        #     # Create the location
        #     ctx['name'] = 'Not in Database'
        #     ctx['location'] = '100 New Location Rd'
        #     response = self.c.post(reverse('core:create_event'), **ctx)
        #     new_event = Event.objects.filter(name=ctx['name']).filter(date=tomorrow)[0]
        #     new_location = Location.objects.filter(address=ctx['location'])[0]
        #     self.assertNotEqual(new_event, None)
        #     self.assertNotEqual(new_location, None)
        #     self.assertRedirects(response, reverse('core:event_stage_two', args=[new_event.id]))
            
            

        # with self.subTest('A location thats in the database'):
        #     # Don't make a duplicate
        #     ctx['name'] = 'In Database'
        #     ctx['location'] = '100 Existing Location Rd'
        #     Location.objects.create(name='Existing Location', address='100 Existing Location Rd')
        #     response = self.c.post(reverse('core:create_event'), **ctx)
        #     new_event = Event.objects.filter(name=ctx['name']).filter(date=tomorrow)[0]
        #     self.assertNotEqual(new_event, None)
        #     self.assertEqual(len(Location.objects.filter(address=ctx['location'])), 1) #Don't create a second one
        #     self.assertRedirects(response, reverse('core:event_stage_two', args=[new_event.id]))
            
            


