from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from .models import Location, Event


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

        self.test_user_ctx = {
            'username': 'test_user',
            'password': 'testuserpass',
            'first_name': 'Test', 
            'last_name': 'User', 
            'email': 'test@email.com'
        }
        self.c = Client()
        self.test_user = User.objects.create(**self.test_user_ctx)
        self.c.force_login(self.test_user)

        self.allison = User.objects.create(first_name='Allison', last_name='Hyatt', email='allison@email.com', username='a-dawg', password='password')
        self.ben = User.objects.create(username='bean', email='b@email.com', first_name='Ben', last_name='Hidden', password='password')
        
        self.casa = Location.objects.create(name='Mi Casa', address='Tortilla Flat')
        self.park = Location.objects.create(name='The Park', address='100 Road St')

        dec1 = timezone.datetime(year=2020, month=12, day=1)
        dec4 = timezone.datetime(year=2020, month=12, day=4)
        self.picnic = Event.objects.create(
            date=dec1,
            time=dec1,
            location=self.park,
            creator=self.allison,
            name='Picnic at the park',
        )
        self.picnic.hosts.add(self.allison)
        self.big_party = Event.objects.create(
            date=dec4,
            time=dec4,
            location=self.casa,
            creator=self.allison,
            name='Bigass Party at my House',
            description='We\'re gonna party our faces off'
        )

    def test_creator_related_name(self):
        self.assertIn(self.big_party, self.allison.events_created.all())
        self.assertIn(self.picnic, self.allison.events_created.all())

    
    def test_location_related_name(self):
        self.assertIn(self.big_party, self.casa.events.all())
        self.assertIn(self.picnic, self.park.events.all())
        self.assertNotIn(self.picnic, self.casa.events.all())

    def test_invited(self):
        self.big_party.invited.add(self.ben)
        with self.subTest('a person is in the events invited list'):
            self.assertIn(self.ben, self.big_party.invited.all())
        with self.subTest('An event is in the persons invited to list'):
            self.assertIn(self.big_party, self.ben.events_invited_to.all())
 
    def test_event_details_view(self):
        ''' Test for the detail view page of a single event'''
        response = self.c.get(f'/event/{self.picnic.id}/')

        # TESTS FOR LOGGED IN USERS
        with self.subTest('The correct details are displayed'):
            self.assertContains(response, f'{self.picnic.name}')
            self.assertContains(response, f'{self.picnic.location}')
            self.assertContains(response, f'{self.picnic.location.address}')
            self.assertContains(response, f'{self.picnic.creator.first_name}')
            # self.assertContains(response, f'{self.picnic.date.FORMAT}')  Need to format

        with self.subTest('An event lists those attending, but not those invited'):
            self.assertNotContains(response, f'{self.ben.username}') # invited, not attending
            self.assertContains(response, f'{self.test_user.username}') # attending
        
        
        # TESTS FOR INVITED USERS
        with self.subTest('An invited user has an "Attend" option'):
            self.big_party.invited.add(self.test_user)
            response = self.c.get(f'/event/{self.picnic.id}/')
            self.assertContains(response, 'Attend')

        # TESTS FOR NON-INVITED USERS
        with self.subTest('A non-invited user does not have an option to attend'):
            self.big_party.invited.add(self.test_user)
            response = self.c.get(f'/event/{self.picnic.id}/')

        # TESTS FOR ATTENDING USERS
        with self.subTest('An attending user has the option of un-RSVPing'):
            self.big_party.attending.add(self.test_user)
            response = self.c.get(f'/event/{self.picnic.id}/')
            self.assertContains(response, "Don't Attend")

        # TESTS FOR THE HOST OF AN EVENT
        with self.subTest('A host has the option of editing the event details'):
            # Log in as host
            self.c.logout()
            a_host = self.picnic.hosts.all()[0]
            credentials = {'username': a_host.username, 'password': a_host.password}
            self.c.login(**credentials)
            # Get new response
            response = self.c.get(f'/event/{self.picnic.id}/')
            
            self.assertContains(response, 'Edit Details')
            edit_url = reverse("core:edit_event", args=[self.picnic.id])
            self.assertContains(response, f'href="{edit_url}"')


        # TESTS FOR LOGGED OUT USERS
        with self.subTest('A logged out user cannot see details'):
            self.c.logout()
            response = self.c.get(f'/event/{self.picnic.pk}/')
            #should redirect to login
            self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('core:event_details', kwargs={'event': self.picnic.pk})}")


           
        
        
