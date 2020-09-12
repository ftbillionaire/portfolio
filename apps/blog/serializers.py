from rest_framework import serializers
from .models import Post, Tag

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'image', 'date_pub', 'tags']

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['title', 'slug', 'date_pub']