from django.shortcuts import render, get_object_or_404
from .models import Prompt, Page, Post, TimeLog
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect
from .forms import TimeLogForm

@method_decorator(login_required, name='dispatch')
class ProgressView(TemplateView):
  template_name = 'website/progress.html'

@method_decorator(login_required, name='dispatch')
class SubmitTimeLogView(FormView):
  template_name = 'website/progress.html'
  form_class = TimeLogForm
  success_url = '/progress/' 

  def form_valid(self, form):
    timelog = form.save(commit=False)
    timelog.user = self.request.user 
    timelog.save()
    return super().form_valid(form)

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

