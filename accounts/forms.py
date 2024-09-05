from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(required=False)


    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UserSignUpForm(UserCreationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control'}
    ))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar']


class UpdateUserForm(forms.ModelForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control', 'id': 'customFile'}
    ))

    class Meta:
        model = Profile
        fields = ['avatar']
