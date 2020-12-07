from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


from django.urls import reverse

class SeleniumTestCase(StaticLiveServerTestCase):
    """
    A base test case for Selenium, providing helper methods for generating
    clients and logging in profiles.
    """

    def open(self, url):
        self.wd.get("%s%s" % (self.live_server_url, url))

    def login(self):
        self.open(reverse('accounts:login'))
        self.wd.find_element(By.ID, 'id_username').send_keys('super_user')
        self.wd.find_element(By.ID, 'button-login').click()


    def wait(self, sec):
        WebDriverWait(self.wd, timeout=sec)
