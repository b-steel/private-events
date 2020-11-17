from django.db import models
from django.utils.translation import gettext as _

class User(models.Model):
    username = models.CharField(_("username"), max_length=50)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    email = models.EmailField(_("email"), max_length=254)
    
