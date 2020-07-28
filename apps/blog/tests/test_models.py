from django.test import TestCase
from django.shortcuts import reverse
from apps.blog.models import *

class TestPostModel(TestCase):
    def setUpTestData():
        Post.objects.create(title = 'Post day')
        Tag.objects.create(title = 'Test tag')

    def tearDown(self):
        tag = Tag.objects.get(id=1)
        tag.delete()

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

    def test_post_many_to_many(self):
        post = Post.objects.get(id=1)
        tag = Tag.objects.get(id=1)
        post.tags.add(tag)
        tag_list = post.tags.all()
        self.assertIn(tag, tag_list)

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

    def test_tag_title_name(self):
        tag = Tag.objects.get(title = 'Tag day')
        field_label = tag._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_tag_date_pub_name(self):
        tag = Tag.objects.get(title = 'Tag day')
        field_label = tag._meta.get_field('date_pub').verbose_name
        self.assertEqual(field_label, "date pub")

    def test_tag_title_max_length(self):
        tag = Tag.objects.get(title = 'Tag day')
        field_length = tag._meta.get_field('title').max_length
        self.assertEqual(field_length, 150)

    def test_tag_slug_max_length(self):
        tag = Tag.objects.get(title = 'Tag day')
        field_length = tag._meta.get_field('slug').max_length
        self.assertEqual(field_length, 100)

    def test_tag_get_absolute_url(self):
        tag = Tag.objects.get(title = 'Tag day')
        slug_end = tag.slug[-10:-1] + tag.slug[-1]
        self.assertEqual(tag.get_absolute_url(), '/tags/tag-day-tag-{}/'.format(slug_end))

    def test_tag_object_name(self):
        tag = Tag.objects.get(title = 'Tag day')
        object_name = str(tag)
        self.assertEqual(object_name, tag.title)
