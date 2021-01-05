from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import View
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings

from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

import requests
import json

from .models import *
from .forms import *
from .serializers import PostSerializer, TagSerializer
# Create your views here.

def main_page(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            subject = "Message from portfolio"
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            body = 'Name: ' + name + '\n' + 'Email: ' + from_email + '\n' + 'Text: ' + form.cleaned_data['body']
            auth_user = 'mysholivsky2003@gmail.com'
            send_mail(subject, body, from_email, [auth_user], fail_silently=False)
            return render(request, 'blog/success.html')
    else:
        form = MailForm()
    return render(request, 'blog/main_page.html', {'form':form})

def posts_list(request):
    search_query = request.GET.get('search', '')
    search_q = str(search_query)
    if search_query:
        posts = Post.objects.filter(Q(title__icontains = search_q) | Q(body__icontains = search_q))
    else:
        posts = Post.objects.all()

    # Pagination
    paginator = Paginator(posts, 5)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)

    return render(request, 'blog/posts_list.html', {'page_obj': page, 'search_q':search_q})

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', {'tags': tags})

def post_detail(request, slug):
    post = Post.objects.get(slug__iexact=slug)
    comments = post.comments.filter(active=True)
    response_data = {}
    if request.is_ajax() and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            body = request.POST.get('body')

            response_data['name'] = name
            response_data['body'] = body

            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.active = True
            new_comment.save()

            return JsonResponse(response_data)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post':post, 'comments': comments, 'form': form,})

def tag_detail(request, slug):
    if request.user.is_staff:
        raise PermissionDenied
    else:
        tag = Tag.objects.get(slug__iexact=slug)
        posts = tag.posts.all()

        paginator = Paginator(posts, 5)
        page_num = request.GET.get('page', 1)
        page = paginator.get_page(page_num)

    return render(request, 'blog/tag_detail.html', {'tag':tag, 'page_obj':page})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-date_pub')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    @action(methods=['get'], detail=False)
    def titles(self, request):
        posts = Post.objects.values()
        ttl=[]
        for post in posts:
            ttl.append(post['title'])
        return Response({'status':'done', 'data':ttl})
# class PostViewSet(viewsets.ViewSet):
#     def list(self, request):
#         posts = Post.objects.values()
#         data = []
#         for post in posts:
#             p = Post.objects.get(id=post['id'])
#             tags = p.tags.values()
#             tag_data = []
#             for tag in tags:
#                 tag_data.append(tag['title'])
#             post['tags']=tag_data
#             data.append(post)
#         return Response({'status':'done', 'data':data})
    
#     def create(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response('Created!')

    # def retrieve(self, request, pk):
    #     try:
    #         user = Post.objects.get(id=pk)
    #         serializer = PostSerializer(user)
    #         data = serializer.data
    #     except:
    #         data=[]
        # posts = Post.objects.values()
        # data = []
        # not_found=[]
        # for post in posts:
        #     if post['id'] == pk:
        #         p = Post.objects.get(id=pk)
        #         tags = p.tags.values()
        #         tag_data = []
        #         for tag in tags:
        #             tag_data.append(tag['title'])
        #         post['tags']=tag_data
        #         data.append(post)
            # else:
            #     error = 'not found'
            #     not_found.append(error)
        # print(not_found)
        # if(len(not_found)>0):
        #     return Response({'status': 'not found', 'data':data})
        # else:
        # return Response({'status':'not found', 'data':data})

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('-date_pub')
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class PostAPIView(UpdateAPIView):
    queryset = Post.objects.all().order_by('-date_pub')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
def getPosts(request):
    posts = Post.objects.values()
    data = []
    for post in posts:
        p = Post.objects.get(id=post['id'])
        tags = p.tags.values()
        tag_data = []
        for tag in tags:
            tag_data.append(tag['title'])
        post['tags']=tag_data
        data.append(post)

    return Response({"message": "Got some data!", "data": data})

@api_view(['GET'])
def getDetailPost(request, pk):
    posts = Post.objects.values()
    data = []
    for post in posts:
        if post['id'] == pk:
            p = Post.objects.get(id=pk)
            tags = p.tags.values()
            tag_data = []
            for tag in tags:
                tag_data.append(tag['title'])
            post['tags']=tag_data
            data.append(post)
        else:
            pass
    return Response({"message": "Got some data!", "data": data})


@api_view(['POST'])
def createPost(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(instance=post, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return Response('Successful operation!')

class PostDetailView(RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()

class TagDetailView(RetrieveAPIView):
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Tag.objects.all()


# def post_crud(request, slug):
#     post = Post.objects.get(slug=slug)

#     if request.method == "GET":
#         serialized = PostSerializer(post)
#         return JsonResponse(serialized)

#     elif request.method == "DELETE":
#         post.delete()
#         return HttpResponse(status=404)