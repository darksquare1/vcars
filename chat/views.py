from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from chat.forms import ChatGroupForm
from chat.models import ChatGroup


class GroupListView(LoginRequiredMixin, ListView):
    model = ChatGroup
    template_name = 'chat/groups_list.html'
    context_object_name = 'groups'
    extra_context = {'form': ChatGroupForm()}

    def post(self, request, *args, **kwargs):
        form = ChatGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            return render(request, 'includes/group_includes.html', {'group': group})


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = ChatGroup
    context_object_name = 'group'
    template_name = 'chat/group_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(ChatGroup, uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.object
        messages = group.message_set.all()
        events = group.event.all()
        context['message_and_event_list'] = sorted([*messages, *events], key=lambda i: i.timestamp)
        context['group_members'] = group.members.all()
        return context

    def get(self, request, *args, **kwargs):
        if request.user not in self.get_object().members.all():
            return HttpResponseForbidden('Вы не присоединены к данному чату')
        return super().get(request, *args, **kwargs)


class CreateGroupView(LoginRequiredMixin, CreateView):
    model = ChatGroup
    template_name = ''
