from django.test import TestCase
from django.shortcuts import reverse
from apps.blog.models import *

class TestPostModel(TestCase):
    def setUpTestData():
        Post.objects.create(title = 'Post day')

    def test_post_title_name(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_post_date_pub_name(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('date_pub').verbose_name
        self.assertEqual(field_label, "date of publication")

    def test_post_title_max_length(self):
        post = Post.objects.get(id=1)
        field_length = post._meta.get_field('title').max_length
        self.assertEqual(field_length, 150)

    def test_post_slug_max_length(self):
        post = Post.objects.get(id=1)
        field_length = post._meta.get_field('slug').max_length
        self.assertEqual(field_length, 100)

    def test_post_get_absolute_url(self):
        post = Post.objects.get(id=1)
        slug_end = post.slug[-10:-1] + post.slug[-1]
        self.assertEqual(post.get_absolute_url(), '/posts/post-day-post-{}/'.format(slug_end))

    def test_post_object_name(self):
        post = Post.objects.get(id=1)
        object_name = str(post)
        self.assertEqual(object_name, post.title)

class TestTagModel(TestCase):
    def setUpTestData():
        Tag.objects.create(title = 'Tag day')
