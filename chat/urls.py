from django.urls import path
from chat.views import GroupListView, GroupDetailView

app_name = 'chat'
urlpatterns = [
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('group/<uuid:uuid>/', GroupDetailView.as_view(), name='group_detail'),
]
