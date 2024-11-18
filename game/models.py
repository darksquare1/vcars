from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
    record = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.record)

    class Meta:
        ordering = ['-record']
