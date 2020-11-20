from django.urls import path

from .views import NewUser, UserDetailView, LoginView, LogoutView

app_name = 'accounts'
urlpatterns = [
    path('new/', NewUser.as_view(), name='signup'),
    path('user/<slug:username>/', UserDetailView.as_view(), name='user_details'), 
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
