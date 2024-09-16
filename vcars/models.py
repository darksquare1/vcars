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


class Comment(models.Model):
    pic = models.ForeignKey(Pic, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
