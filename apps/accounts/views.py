from django.shortcuts import render
from django import views

from .forms import SigninForm, UserForm


class NewUser(views.View):
    def get(self, request):
        form = UserForm()
        return render(request, 'accounts/new_user.html', {'form': form})