from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_images')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.avatar.path)
        size = (100, 100)
        if img.height > 100 or img.width > 100:
            img.thumbnail(size)
            img.save(self.avatar.path)
