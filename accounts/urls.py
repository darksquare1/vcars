from django.urls import path
from accounts.views import SignUpView, CustomLoginView, ProfileDetailView, ProfileUpdateView, VerifyView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html'),
         name='login'),
    path('profile/<slug:slug>/', ProfileDetailView.as_view(), name='profile'),
    path('profile-edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('verify/<uuid>', VerifyView.as_view(), name='verify'),

]
