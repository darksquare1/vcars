from email.headerregistry import Group

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from chat.models import ChatGroup


class GroupListView(LoginRequiredMixin, ListView):
    model = ChatGroup
    template_name = 'chat/groups_list.html'
    context_object_name = 'groups'


