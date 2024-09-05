from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import UserSignUpForm, UserLoginForm


class SignUpView(generic.CreateView):
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('vcars:index')


class CustomLoginView(LoginView):
    form_class = UserLoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        print('bye')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


