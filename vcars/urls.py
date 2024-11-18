from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from config import settings
from . import views
from .views import LikeView

app_name = 'vcars'
urlpatterns = [
    path('', views.PictureListView.as_view(), name='index'),
    path('tag/<slug:tag_slug>/', views.PictureListView.as_view(), name='tagged_index'),
    path('pic/<slug:slug>/', views.PicDetailView.as_view(), name='pic_detail'),
    path('addpic/', views.CreatePic.as_view(), name='post_pic'),
    path('rating/', LikeView.as_view(), name='rating'),

]
