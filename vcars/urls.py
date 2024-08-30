from django.conf.urls.static import static
from django.urls import path

from config import settings
from . import views

app_name = 'vcars'
urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<slug:tag_slug>/', views.index, name='tagged_index'),
    path('pic/<int:pic_id>/', views.pic_detail, name='pic_detail'),
    path('addpic/', views.post_pic, name='post_pic')
]
