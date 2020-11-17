from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone

class User(models.Model):
    username = models.CharField(_("username"), max_length=50, unique=True)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    email = models.EmailField(_("email"), max_length=254)
    created_at = models.DateField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    
