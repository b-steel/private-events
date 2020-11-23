from django.urls import path, include
from . import views

app_name ='core'
urlpatterns = [
    path('event/index/', views.EventIndexView.as_view(), name='event_index'),
    # path('event/create_event/', PLACEHOLDER, name='create_event'),
    # path('event/<slug:event_id>/show/', PLACEHOLDER, name='event_details'),
    # path('event/<slug:event_id>/edit/', PLACEHOLDER, name='edit_event'),
    # path('event/<slug:event_id>/stage2/', PLACEHOLDER, name='event_stage_two'),
    # path('get_potential_invites/', PLACEHOLDER, name='get_potential_invites'), 
    # path('get_potential_hosts/', PLACEHOLDER, name='get_potential_hosts'),
]
