from django.shortcuts import render, redirect
from django.urls import reverse
from django import views
from django.views.generic.detail import DetailView

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
            return redirect(reverse('accounts:user_details'), args=[user.pk])


class UserDetailView(DetailView):
    model = User
    template_name = "accounts/user_details.html"
