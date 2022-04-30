from dataclasses import dataclass
from unicodedata import category
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import pre_save
from BlogPage.utils import unique_slug_generator

class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Category(models.Model):
    word = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    probability = models.FloatField(default=0)

    def __str__(self):
        return self.word

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, default=User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    intro = models.TextField()
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    dislikes = models.ManyToManyField(User, related_name='blog_post')
    views = models.ManyToManyField(IpModel, related_name='post_views', blank=True)
    categories = models.ManyToManyField(Category, related_name='posts')

    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()

    def total_views(self):
        return self.views.count()

    def timeToRead(self):
        if int(len(self.body.split())/238) == 0:
            return "< 1"
        return int(len(self.body.split())/238)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date_added']

    def datepublished(self):
        return self.date_added.strftime('%d %B %Y')

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    subscribers = models.ManyToManyField(User, related_name='subscribers')
    categories_liked = models.ManyToManyField(Category, related_name='categories_liked')
    categories_disliked = models.ManyToManyField(Category, related_name='categories_disliked')
    history = models.ManyToManyField(Post, related_name='history')
    reputation = models.FloatField(default=1)

    def total_subscribers(self):
        return self.subscribers.count()

    def __str__(self):
        return self.user.username

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

    def __str__(self):
        return self.user.username + ': ' + self.content
        
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)