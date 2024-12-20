from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from django.views.generic import DetailView, UpdateView, View

from accounts.forms import UserSignUpForm, UserLoginForm, UpdateUserForm, UpdateProfileForm
from accounts.models import Profile


class SignUpView(generic.CreateView):
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'

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
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'registration/profile.html'
    context_object_name = 'profile'


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'registration/profile_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['user_form'] = UpdateUserForm(instance=self.request.user)
        else:
            context['user_form'] = UpdateUserForm(instance=self.request.user, data=self.request.POST)
        return context

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if form.is_valid() and user_form.is_valid():
                user_form.save()
                form.save()
            else:
                context['user_form'] = user_form
                return self.render_to_response(context)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', args=[self.object.slug])


class VerifyView(View):
    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        try:
            user = User.objects.get(profile__is_verified=False, profile__verification_uuid=uuid)
        except User.DoesNotExist:
            raise Http404('Пользователь не существует или уже был верифицирован')

        user.profile.is_verified = True
        user.profile.save()
        return render(request, 'registration/verify.html')
