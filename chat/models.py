from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from uuid import uuid4


class ChatGroup(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=25)
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'Group {self.name}-{self.uuid}'

    def get_absolute_url(self):
        return reverse('chat:group', args=[self.uuid])

    def add_user_to_group(self, user):
        self.members.add(user)
        self.event.create(type=Event.EventChoice.JOIN, user=user)
        self.save()

    def remove_user_from_group(self, user):
        self.members.remove(user)
        self.event.create(type=Event.EventChoice.LEFT, user=user)
        self.save()

    class Meta:
        ordering = ['created_at']


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)

    def __str__(self):
        date = self.timestamp.date()
        time = self.timestamp.time()
        return f"{self.author}:- {self.body} @{date} {time.hour}:{time.minute}"


class Event(models.Model):
    class EventChoice(models.TextChoices):
        JOIN = 'Join', 'join'
        LEFT = 'Left', 'left'

    type = models.CharField(choices=EventChoice.choices, max_length=10)
    description = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='event')

    def save(self, *args, **kwargs):
        self.description = f'{self.user.username} {self.type} the {self.group.name} group'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
