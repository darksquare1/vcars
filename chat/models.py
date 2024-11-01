from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from uuid import uuid4


class ChatGroup(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=25)
    members = models.ManyToManyField(User)
    def __str__(self):
        return f'Group {self.name}-{self.uuid}'
    def get_absolute_url(self):
        return reverse('chat:group', args=[str(self.uuid)])
    def add_user_to_group(self, user):
        self.members.add(user)
        self.event.create(type='Join', user=user)
        self.save()
    def remove_user_from_group(self, user):
        self.members.remove(user)
        self.event.create(type='Left', user=user)
        self.save()
