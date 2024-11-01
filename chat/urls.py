from django.urls import path
from chat.views import GroupListView

app_name = 'chat'
urlpatterns = [
    path('groups/', GroupListView.as_view(), name='group_list'),
]
