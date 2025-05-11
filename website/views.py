from django.shortcuts import render, get_object_or_404
from .models import Prompt, Page, Post, Language, TabooSet, Word, TabooCard, TabooCardTabooWord, Level
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from django.shortcuts import render, redirect
from .forms import TimeLogForm
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from .openai.api import generate_set
from django.contrib import messages


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
  # prompts = Prompt.objects.filter(user__organisation=request.organisation)
  # For now, show all the prompts in the org's main language
  prompts = Prompt.objects.filter(language=request.organisation.language)
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

def unspeakable(request):
  return render(request, 'website/unspeakable.html')

def dashboard_view(request):
  languages = Language.objects.all()
  levels = Level.objects.all()

  cards = request.session.get("generated_cards")
  selected_language = None
  selected_theme = request.session.get("selected_theme")

  if language_id := request.session.get("selected_language_id"):
    try:
      selected_language = Language.objects.get(pk=language_id)
    except Language.DoesNotExist:
      pass

  return render(request, "website/dashboard.html", {
    "languages": languages,
    "levels": levels,
    "cards": cards,
    "selected_language": selected_language,
    "selected_theme": selected_theme,
  })


@require_POST
def generate_set_view(request):
  MAX_CALLS_PER_SESSION = 3
  session = request.session
  session.setdefault('openai_call_count', 0)
  
  if session['openai_call_count'] >= MAX_CALLS_PER_SESSION:
    messages.error(request, 'You’ve reached the maximum number of sets for this session.')
    return redirect("dashboard")

  language_id = request.POST.get("language")
  theme = request.POST.get("theme", "").strip()
  level_id = request.POST.get("level")
  count = int(request.POST.get("count", 30))

  try:
    language = Language.objects.get(pk=language_id)
    level = Level.objects.get(pk=level_id)
    generated = generate_set(language.name, theme, count, level.code)

    session["generated_cards"] = generated['cards']
    session["selected_language_id"] = language.id
    session["selected_theme"] = theme
    session['openai_call_count'] += 1
    session.modified = True

    messages.success(request, f"Generated {len(generated['cards'])} cards for theme '{theme}' in {language.name}.")
  except Exception as e:
    messages.error(request, f"❌ Generation failed: {str(e)}")

  return redirect("dashboard")

@require_POST
def save_set_view(request):
  session = request.session
  cards = request.session.get("generated_cards")
  lang_id = request.session.get("selected_language_id")
  theme = request.session.get("selected_theme")

  if not cards or not lang_id:
    messages.error(request, "⚠️ No cards to save — please generate first.")
    return redirect("dashboard")

  try:
    language = Language.objects.get(pk=lang_id)
    taboo_set = TabooSet.objects.create(
      name=f"{theme.title()} ({language.name})",
      owner=request.user,
      language=language
  )

    for card_data in cards:
      target_word, _ = Word.objects.get_or_create(
        word=card_data["target"].strip().lower(),
        language=language,
        defaults={"part_of_speech": "noun"}
      )
      card = TabooCard.objects.create(taboo_set=taboo_set, target=target_word)

      for taboo in set(card_data["taboo_words"]):
        taboo_word, _ = Word.objects.get_or_create(
          word=taboo.strip().lower(),
          language=language,
          defaults={"part_of_speech": "noun"}
        )
        TabooCardTabooWord.objects.create(card=card, taboo_word=taboo_word)

      for key in ["generated_cards", "selected_language_id", "selected_theme"]:
        session.pop(key, None)

      messages.success(request, f"✅ Set '{taboo_set.name}' saved with {len(cards)} cards.")
  except Exception as e:
    messages.error(request, f"❌ Failed to save set: {str(e)}")

  return redirect("dashboard")
