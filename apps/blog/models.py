from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time

# Create your models here.

def gen_slug(model_title, model_name):
    new_slug = slugify(model_title, allow_unicode = True)
    return new_slug + '-' + model_name + '-' + str(int(time()))

class Post(models.Model):
    title = models.CharField(max_length = 150, db_index =True)
    slug = models.SlugField(max_length = 100, blank=True, unique = True)
    body = models.TextField(blank = True, db_index = True)
    image = models.ImageField(upload_to = 'images', blank = True)
    tags = models.ManyToManyField('Tag', blank = True, related_name = 'posts')
    date_pub = models.DateField(auto_now_add = True, verbose_name = "date of publication")

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title, Post._meta.model_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug':self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering=['-id']

class Tag(models.Model):
    title = models.CharField(max_length = 150, db_index = True)
    slug = models.SlugField(max_length = 100, blank = True, unique = True)
    date_pub = models.DateField(auto_now_add = True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title, Tag._meta.model_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug':self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']

class Comment(models.Model):
    name = models.CharField(max_length = 30, db_index = True)
    body = models.TextField()
    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = 'comments')
    date_pub = models.DateField(auto_now_add = True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "Comment '{}' by {}".format(self.body, self.name)

    class Meta:
        ordering = ['-id']
