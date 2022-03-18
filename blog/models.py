from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import pre_save
from BlogPage.utils import unique_slug_generator

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, default=User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    intro = models.TextField()
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def datepublished(self):
        return self.date_added.strftime('%d %B %Y')

class Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def datepublished(self):
        return self.date_added.strftime('%d %B %Y')

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)