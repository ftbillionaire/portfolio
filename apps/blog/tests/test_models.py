from django.test import TestCase
from django.shortcuts import reverse
from apps.blog.models import *

class TestPostModel(TestCase):
    def setUpTestData():
        post = Post.objects.create(title = 'Post', slug = 'post-sl')
        print(post.title)

    def test_post_get_absolute_url(self):
        post = Post.objects.get(title = 'Post')
        self.assertEqual(post.get_absolute_url(), '/posts/post-sl/')
