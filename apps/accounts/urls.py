from django.urls import path

from .views import NewUser

urlpatterns = [
    path('new/', NewUser.as_view(), name='new_user'),
]
