from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('new/', views.NewUser.as_view(), name='signup'),
    path('user/<slug:username>/', views.UserDetailView.as_view(), name='user_details'), 
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]
