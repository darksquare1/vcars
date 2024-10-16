from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image

from services.utils import unique_slugify


class PicManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('tags')


class Pic(models.Model):
    tags = TaggableManager()
    name = models.CharField(max_length=25)
    body = models.TextField()
    pic = models.ImageField(upload_to='images',
                            validators=[FileExtensionValidator(allowed_extensions=['jpg', 'webp', 'jpeg', 'png'])])
    thumb = models.CharField(max_length=120, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, blank=True)
    objects = models.Manager()
    custom = PicManager()

    class Meta:
        ordering = ['-creation_time']
        indexes = [models.Index(fields=['-creation_time'])]

    def get_absolute_url(self):
        return reverse('vcars:pic_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)
        img = Image.open(self.pic.path)
        if img.height > 320 or img.width > 320:
            img.thumbnail((320, 320))
            thumb = f'media/thumbs/{self.id}.{img.format}'

            img.save(thumb)
            Pic.objects.filter(id=self.id).update(thumb=thumb)

    def count_rating(self):
        return sum([rating.rating for rating in self.ratings.all()])

    def __str__(self):
        return self.name


class Comment(models.Model):
    pic = models.ForeignKey(Pic, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=64)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]


class Rating(models.Model):
    pic = models.ForeignKey(Pic, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField(choices=[(1, 'Нравится'), (2, 'Не нравится')])
    created = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()

    class Meta:
        unique_together = ('pic', 'ip')
        ordering = ('-created',)
        indexes = [models.Index(fields=['created', 'rating'])]

