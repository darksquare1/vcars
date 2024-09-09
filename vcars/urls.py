from django.conf.urls.static import static
from django.urls import path

from config import settings
from . import views

app_name = 'vcars'
urlpatterns = [
    path('', views.PictureListView.as_view(), name='index'),
    path('tag/<slug:tag_slug>/', views.PictureListView.as_view(), name='tagged_index'),
    path('pic/<int:pic_id>/', views.PicDetailView.as_view(), name='pic_detail'),
    path('addpic/', views.post_pic, name='post_pic'),


]
