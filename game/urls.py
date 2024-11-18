from django.urls import path
from game.views import GameView, RecordView

app_name = 'game'
urlpatterns = [
    path('game/', GameView.as_view(), name='game'),
    path('save-record/', RecordView.as_view(), name='save_record')
]
