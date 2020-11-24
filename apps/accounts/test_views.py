from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from apps.core.models import User
from django.utils import timezone
from django.urls import reverse


from apps.core.models import Location, Event
from .views import NewUser, UserDetailView, LoginView, LogoutView, HomePageView


class NotAuthenticatedTestCase(TestCase):

    def setUp(self):
        self.user_ctx = {
            'username': 'test_user',
            'password': 'testuserpass',
            'first_name': 'Test', 
            'last_name': 'User', 
            'email': 'test@email.com'
        }
        self.c = Client()
        self.test_user = User.objects.create(**self.user_ctx)
        self.test_location = Location.objects.create(name='place', address=
        'somewhere')
        self.test_event = Event.objects.create(creator=self.test_user, location=self.test_location, name='event name', description='event desc', date=timezone.now(), time=timezone.now())

    def test_navbar_not_authenticated_links(self):
        ''' A user who is not logged in should see login and sign up'''
        response = self.c.get('/home/')
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Sign Up')


    def test_navbar_not_authenticated_no_logout(self):
        ''' A user who is not logged in should not see logout'''
        response = self.c.get('/home/')
        self.assertNotContains(response, 'Logout')

    def test_navbar_not_authenticated_no_profile_link(self):
        ''' A user who is not logged in should not see a welcome message / link to their profile'''
        response = self.c.get('/home/')
        self.assertNotContains(response, r'href="{% url \'accounts:user_details\' %}"')

    def test_navbar_not_authenticated_no_profile_view(self):
        ''' A user who is not logged in should not be able to see info about another user'''

        response = self.c.get(f'/accounts/user/{self.test_user.username}/')
        self.assertRedirects(response, f'{reverse("accounts:login")}?next={reverse("accounts:user_details", kwargs={"username":self.test_user.username})}')
    

class AuthenticatedTestCase(TestCase):
    def setUp(self):
        self.user_ctx = {
            'username': 'test_user',
            'password': 'testuserpass',
            'first_name': 'Test', 
            'last_name': 'User', 
            'email': 'test@email.com'
        }
        self.c = Client()
        self.test_user = User.objects.create(**self.user_ctx)
        self.c.force_login(self.test_user)
        self.test_location = Location.objects.create(name='place', address=
        'somewhere')
        self.test_event = Event.objects.create(creator=self.test_user, location=self.test_location, name='event name', description='event desc', date=timezone.now(), time=timezone.now())
    def test_navbar_authenticated(self):
        ''' A logged in user should see a link to their page and a 'logout' link'''
        
        response = self.c.get('/home/')

        self.assertNotContains(response, 'Login')
        self.assertContains(response, 'Logout')
        self.assertContains(response, f'href="{reverse("accounts:user_details", kwargs={"username": self.test_user.username})}"')

    def test_authenticated_can_see_user_details(self):
        ''' A logged in user should be able to see another users details'''
        
        response = self.c.get(f'/accounts/user/{self.test_user.username}/')

        self.assertContains(response, 'test_user') # we're on the right profile
        self.assertContains(response, 'test@email.com') # should have their details
        self.assertContains(response, 'event name') # should show the events the user has created



