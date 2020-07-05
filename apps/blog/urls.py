from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage.send_us),
    path('', MainPage.main_page, name = 'main_page_url'),
    path('posts/', posts_list, name = 'posts_list_url'),
    path('tags/', tags_list, name = 'tags_list_url'),
    path('posts/<str:slug>/', post_detail, name = 'post_detail_url'),
    path('tags/<str:slug>/', tag_detail, name = 'tag_detail_url')
]
