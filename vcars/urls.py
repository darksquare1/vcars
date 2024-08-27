from django.conf.urls.static import static
from django.urls import path

from config import settings
from . import views

app_name = 'vcars'
urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<slug:tag_slug>/', views.index, name='tagged_index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
