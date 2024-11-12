from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import Profile


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Пароль')
    remember_me = forms.BooleanField(required=False, label='Запомнить меня')

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
    first_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с такой почтой уже существует')
        return email

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'avatar']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'Почта должна быть уникальной')
        return email


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control', 'id': 'customFile'}
    ))
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    bio = forms.CharField(max_length=500,
                          widget=forms.Textarea(attrs={'rows': 5, "class": "form-control"}), required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'birth_date']
