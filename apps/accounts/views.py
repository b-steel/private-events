from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django import views
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from apps.core.models import User
from .forms import LoginForm, UserForm


class NewUser(views.View):
    def get(self, request):
        form = UserForm()
        return render(request, 'accounts/new_user.html', {'form': form})
    
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('accounts:user_details', kwargs={'username':user.username}))


class UserDetailView(LoginRequiredMixin, views.View):
    # Available info from urls.py <slug:username>
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        ctx = {
            'profile': user,
            'attending_events': user.events_attending.filter(date__gte=timezone.now()),
            'attended_events': user.events_attending.filter(date__lt=timezone.now()),
        }
        return render(request, 'accounts/user_details.html', ctx)

class InvitationsView(LoginRequiredMixin, views.View):
    def get(self, request):
        return render(request, 'accounts/invitations.html')

class LoginView(views.View):
    def get(self, request):
        form = LoginForm()
        redirect_to = request.GET.get('next', '')
        redirected = False
        if redirect_to != '':
            redirected = True

        return render(request, 'accounts/login.html', {'form': form, 'redirect': redirected}) 
    
    def post(self, request):
        bound_form = LoginForm(request.POST)
        if bound_form.is_valid():
            user = User.objects.get(username=bound_form.cleaned_data['username'])
            login(request, user)
            redirect_to = request.POST.get('next')
            if redirect_to:
                return redirect(redirect_to)
            return render(request, 'accounts/success.html', {})
        else:
            return render(request, 'accounts/login.html', {'form': bound_form})


class LogoutView(views.View):
    def get(self, request):
        logout(request)
        return render(request, 'accounts/logout_success.html')

class HomePageView(TemplateView):

    template_name='accounts/home.html'



