from .selenium_test_case import SeleniumTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


from django.urls import reverse
from django.utils import timezone
from .utils import ModelFactory

class SeleniumTests(SeleniumTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wd = WebDriver()
        cls.mf = ModelFactory()
        cls.su = cls.mf.users.new(username='super_user')

    @classmethod
    def tearDownClass(cls):
        cls.wd.quit()
        super().tearDownClass()

    def setUp(self):
        self.login()
        
    def test(self):
        with self.subTest('Create a new event'):
            self.open(reverse('core:create_event'))
            WebDriverWait(self.wd, timeout=3).until(lambda d: d.find_element(By.XPATH, "//button[@type='submit']"))
            form = self.wd.find_element(By.TAG_NAME, 'form')
            name = form.find_element(By.ID, 'id_name').send_keys('Selenium Test Event')
            description = self.wd.find_element(By.ID, 'id_description').send_keys('This event created by Selenium')
            date = self.wd.find_element(By.ID, 'id_date').send_keys((timezone.now()+timezone.timedelta(days=1)).strftime('%m/%d/%Y'))
            location = self.wd.find_element(By.ID, 'id_location').send_keys('Here or There')

            button = form.find_element(By.XPATH, "//button[@type='submit']").click()
            # modal = self.wd.find_element(By.ID, 'button-open-modal').click()
            
            # Should redirect to the event
            self.assertIn('Event Details', self.wd.title)


        with self.subTest('Look at an events details'):
            event = self.mf.events.new(name='First Event', date='future')
            
            self.open(reverse("core:index"))
            href = reverse('core:event_details', kwargs={'event_id':event.pk})
            self.wd.find_element(By.XPATH, f"//a[@href='{href}']").click()
            #should got to the details for the new event
            self.assertIn(event.location, self.wd.find_element(By.ID, 'event-location').text)

    def test_c_new_user(self):
        self.logout() # make sure we're logged out
        self.open(reverse("accounts:signup"))
        form = self.wd.find_element(By.TAG_NAME, 'form')
        username = form.find_element(By.ID, 'id_username').send_keys('new_user')
        first_name = form.find_element(By.ID, 'id_first_name').send_keys('New')
        last_name = form.find_element(By.ID, 'id_last_name').send_keys('User')
        submit = form.find_element(By.TAG_NAME, 'button').click()
        
        with self.subTest('After user creation we should be redirected to the user details page'):
            self.assertEqual(self.wd.title, 'User Details | EventLite')

        with self.subTest('The new user can log out'):
            self.wd.find_element(By.ID, 'link-logout').click()
            self.assertEqual(self.wd.title, 'Logout Success | EventLite')
            
            # Wait for the redirect
            WebDriverWait(self.wd, timeout=4).until(lambda d: 'Index' in d.title)

        with self.subTest('The new user can log in'):
            WebDriverWait(self.wd, timeout=3).until(lambda d: d.find_element(By.ID, 'link-login'))
            self.wd.find_element(By.ID, 'link-login').click()
            self.wd.find_element(By.ID, 'id_username').send_keys('new_user' + Keys.ENTER)
            WebDriverWait(self.wd, timeout=1).until(lambda d: 'Success' in d.title)
            self.assertIn('Success', self.wd.find_element(By.TAG_NAME, 'p').text)
            
            # Wait for the redirect
            WebDriverWait(self.wd, timeout=3).until(lambda d: 'Index' in d.title)


            

