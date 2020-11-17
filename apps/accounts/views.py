from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django import views
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SigninForm, UserForm
from .models import User


class NewUser(views.View):
    def get(self, request):
        form = UserForm()
        return render(request, 'accounts/new_user.html', {'form': form})
    
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('accounts:user_details', kwargs={'username':user.username}))


class UserDetailView(views.View):
    # Available info from urls.py <slug:username>
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        return render(request, 'accounts/user_details.html', {'object': user})
        
