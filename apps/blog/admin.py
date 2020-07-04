from django.contrib import admin
from .models import *
# Register your models here.
class PostInfo(admin.ModelAdmin):
    list_display = ('title', 'slug','date_pub')
    list_filter = ('tags', 'date_pub')

class TagInfo(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_pub')


admin.site.register(Post, PostInfo)
admin.site.register(Tag, TagInfo)
