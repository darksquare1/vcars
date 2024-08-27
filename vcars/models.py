from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image


class Pic(models.Model):
    tags = TaggableManager()
    name = models.CharField(max_length=25)
    body = models.TextField()
    pic = models.ImageField(upload_to='images')
    thumb = models.CharField(max_length=120, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creation_time']
        indexes = [models.Index(fields=['-creation_time'])]

    def get_absolute_url(self):
        return reverse('vcars:pic_detail', args=[self.id])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.pic.path)
        if img.height > 15250 or img.width > 15520:
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
