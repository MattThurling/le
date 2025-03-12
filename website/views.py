from django.shortcuts import render, get_object_or_404
from .models import Prompt, Page, Post

def index(request):
  return render(request, 'website/index.html')

def prompt_list(request):
  prompts = Prompt.objects.all()
  return render(request, 'website/prompts.html', {'prompts': prompts})

def page_list(request):
  pages = Page.objects.all()
  return render(request, 'website/pages.html', {'pages': pages})

def post_list(request):
  posts = Post.objects.all()
  return render(request, 'website/posts.html', {'posts': posts})

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)
  return render(request, 'website/post.html', {'post': post})

