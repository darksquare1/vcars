from django.urls import path
from vcars_api import views

app_name = 'api_vcars'
urlpatterns = [
    path('', views.GetPicsApiView.as_view(), name='list-pics'),
    path('pic/<slug:slug>/', views.RetrievePicApiView.as_view(), name='retrieve-pic'),
    path('add/comment/',views.AddCommentApiView.as_view(), name='write-comment'),
    path('add/pic', views.AddPicApiView.as_view(), name='add-pic')
]