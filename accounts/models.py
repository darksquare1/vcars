import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from PIL import Image
from services.utils import unique_slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default='default.png', upload_to='profile_images',
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'webp', 'jpeg', 'png'])])
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        size = (100, 100)
        if img.height > 100 or img.width > 100:
            img.thumbnail(size)
            img.save(self.avatar.path)

    def get_absolute_url(self):
        return reverse('profile', args=[self.slug])

    def is_online(self):
        cache_key = f'last-seen-{self.user.id}'
        last_seen = cache.get(cache_key)
        if last_seen is not None:
            return True
        return False
