from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', main_page, name = 'main_page_url'),
    path('posts/', posts_list, name = 'posts_list_url'),
    path('tags/', tags_list, name = 'tags_list_url'),
    path('posts/<str:slug>/', post_detail, name = 'post_detail_url'),
    path('tags/<str:slug>/', tag_detail, name = 'tag_detail_url'),
    path('api/', include(router.urls))
]
