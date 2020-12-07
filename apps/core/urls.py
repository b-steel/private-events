from django.urls import path, include
from . import views

app_name ='core'
urlpatterns = [
    path('index/', views.EventIndexView.as_view(), name='index'),
    path('event/new/', views.CreateEventView.as_view(), name='create_event'),
    path('event/<slug:event_id>/show/', views.EventDetailView.as_view(), name='event_details'),
    # path('event/<slug:event_id>/edit/', PLACEHOLDER, name='edit_event'),
    # path('event/<slug:event_id>/stage2/', PLACEHOLDER, name='event_stage_two'),
    # path('get_potential_invites/', PLACEHOLDER, name='get_potential_invites'), 
    # path('get_potential_hosts/', PLACEHOLDER, name='get_potential_hosts'),
    path('ajax/invite_users/', views.ajax_invite_users, name='ajax_invite_users'),
    path('ajax/accept_invite/', views.ajax_accept_invite, name='ajax_accept_invite'),

]
