from django.urls import path
from . import views

app_name = 'vcars'
urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<slug:tag_slug>/', views.index, name='tagged_index')
]
