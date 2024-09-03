from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import UserSignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SignUpView(generic.CreateView):
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
