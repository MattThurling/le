from django.shortcuts import render, get_object_or_404
from .models import Prompt, Page, Post, TimeLog
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from django.shortcuts import render, redirect
from .forms import TimeLogForm
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.views import LoginView

def register_view(request):
    if request.user.is_authenticated:  # Redirect if already logged in
        return redirect('progress')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registering
            return redirect('progress')
        else:
            print("Form errors:", form.errors)
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # Redirect if already logged in
            return redirect('progress')
        return super().get(request, *args, **kwargs)

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
  org_filter = request.GET.get('o', None)  # Get the 'o' parameter from the URL
  if org_filter:
    prompts = Prompt.objects.filter(organisation=org_filter)
  else:
    prompts = Prompt.objects.filter(organisation__isnull=True)
  return render(request, 'website/prompts.html', {'prompts': prompts})

def prompt_detail(request, slug):
  prompt = get_object_or_404(Prompt, slug=slug)
  return render(request, 'website/prompt.html', {'prompt': prompt})

def page_list(request):
  pages = Page.objects.all()
  return render(request, 'website/pages.html', {'pages': pages})

def post_list(request):
  posts = Post.objects.all()
  return render(request, 'website/posts.html', {'posts': posts})

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)
  return render(request, 'website/post.html', {'post': post})

