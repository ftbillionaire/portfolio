from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet, basename='post')
# router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', main_page, name = 'main_page_url'),
    path('posts/', posts_list, name = 'posts_list_url'),
    path('tags/', tags_list, name = 'tags_list_url'),
    path('posts/<str:slug>/', post_detail, name = 'post_detail_url'),
    path('tags/<str:slug>/', tag_detail, name = 'tag_detail_url'),
    path('api/', include(router.urls)),
    ## viewset
    # path('api/posts/', PostViewSet.as_view({'get':'list'})),
    # path('api/post/<int:pk>/', PostViewSet.as_view({'get':'retrieve'})),
    ## api_view
    # path('api/create/post', createPost, name = 'create_post'),
    # path('api/update/post/<int:pk>/', updatePost, name = 'update_post'),
    # path('api/delete/post/<int:pk>/', deletePost, name = 'delete_post'),
    # path('api/post/<int:pk>', getDetailPost, name = 'get-detail_post'),
    # path('api/posts/', getPosts, name = 'get_posts')
    ## APIView
    # path('api/posts/<int:pk>/', PostDetailView.as_view()),
    # path('api/tags/<int:pk>/', TagDetailView.as_view()),
    # path('api/update/post/<int:pk>/', PostAPIView.as_view(), name = 'update_post'),
]