from django.urls import path

from .views import NewUser, UserDetailView

app_name = 'accounts'
urlpatterns = [
    path('new/', NewUser.as_view(), name='new_user'),
    path('user/<slug:username>/', UserDetailView.as_view(), name='user_details')
]
