from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from bs4 import BeautifulSoup
import requests

from .models import *
from .forms import *
# Create your views here.

def auth_menu(request):
    form = CreateUserForm()
    return render(request, 'auth/sign_up.html', {'form':form})

class MainPage(View):
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

        url = "https://www.worldometers.info/coronavirus/"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        stats = []
        new_stats = []
        stats = soup.findAll('div', class_ = "maincounter-number")
        article = ["Cases", "Deaths", "Recovered"]
        for i in range(len(stats)):
            new_stats.append(stats[i].text)
        return render(request, 'blog/main_page.html', {'form':form, 'stats':new_stats, 'article':article})

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
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.active = True
            new_comment.save()
            return redirect('post_detail_url', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post':post, 'comments': comments, 'form': form})

def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    posts = tag.posts.all()

    paginator = Paginator(posts, 5)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)

    return render(request, 'blog/tag_detail.html', {'tag':tag, 'page_obj':page})
