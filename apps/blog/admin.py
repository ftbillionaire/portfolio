from django.contrib import admin

from .models import *
# Register your models here.
@admin.register(Post)
class PostInfo(admin.ModelAdmin):
    list_display = ('title', 'slug','date_pub')
    list_filter = ('tags', 'date_pub')

@admin.register(Tag)
class TagInfo(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_pub')

@admin.register(Comment)
class CommentInfo(admin.ModelAdmin):
    list_display = ('name', 'date_pub', 'post', 'active')
    list_filter = ('name', 'date_pub', 'post', 'active')
