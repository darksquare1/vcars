from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import UserSignUpForm, UserLoginForm, UpdateUserForm, UpdateProfileForm
from accounts.models import Profile


class SignUpView(generic.CreateView):
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        profile1 = Profile(user=user)
        avatar = self.request.FILES.get('avatar', None)
        if avatar:
            user.profile.avatar = avatar
        user.save()
        profile1.save()
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


@login_required
def profile(request):
    if request.method == 'GET':
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    else:
        user_form = UpdateUserForm(instance=request.user, data=request.POST)
        profile_form = UpdateProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    return render(request, 'registration/profile.html', {'user_form': user_form, 'profile_form': profile_form})
