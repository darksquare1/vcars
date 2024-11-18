from django.urls import path
from django.views.generic import TemplateView

app_name = 'game'
urlpatterns = [
    path('game/', TemplateView.as_view(template_name='game/game.html'), name='game')
]