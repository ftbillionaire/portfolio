from django.db import models
from django.shortcuts import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 150, db_index =True)
    slug = models.SlugField(max_length = 100, unique = True)
    body = models.TextField(blank = True, db_index = True)
    image = models.ImageField(upload_to = 'images', blank = True)
    tags = models.ManyToManyField('Tag', blank = True, related_name = 'posts')
    date_pub = models.DateField(auto_now_add = True, verbose_name = "date of publication")

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug':self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering=['-id']

class Tag(models.Model):
    title = models.CharField(max_length = 150, db_index = True)
    slug = models.SlugField(max_length = 100, unique = True)
    date_pub = models.DateField(auto_now_add = True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug':self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']

class Comment(models.Model):
    name = models.CharField(max_length = 100, db_index = True)
    body = models.TextField(db_index = True)
    date_pub = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_pub']
