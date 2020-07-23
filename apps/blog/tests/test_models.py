from django.test import TestCase
from django.shortcuts import reverse
from apps.blog.models import *

class TestPostModel(TestCase):
    def setUpTestData():
        Post.objects.create(title = 'Post')
        print('.')
        print('Post was created!')

    def test_post_get_absolute_url(self):
        post = Post.objects.get(title = 'Post')
        slug_end = post.slug[-10:-1] + post.slug[-1]
        self.assertEqual(post.get_absolute_url(), '/posts/post-post-{}/'.format(slug_end))
