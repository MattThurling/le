from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from tinymce.models import HTMLField
from django.urls import reverse
from django.utils.text import slugify

class BaseModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True
    ordering = ['-updated_at']

class ImageModel(BaseModel):
  image = models.CharField(max_length=255, null=True, blank=True)

  @property
  def image_url(self):
    return f"{settings.STORAGE_ROOT_URL}{self.image}"

  class Meta:
    abstract = True

class Language(ImageModel):
  name = models.CharField(max_length=64)

  def __str__(self):
    return self.name

class Organisation(ImageModel):
  name = models.CharField(max_length=100)
  domain = models.CharField(max_length=255, unique=True)
  language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="organisations")

  def __str__(self):
    return self.name

class User(AbstractUser):
  organisation = models.ForeignKey(
    Organisation,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name='users',
  )

  def get_attainments(self):
    return self.attainments.select_related('level').all()

  def get_current_and_next_level(self):
    latest_attainment = (
      self.attainments.select_related('level')
      .order_by('-level__hierarchy')
      .first()
    )

    if latest_attainment:
      current_level = latest_attainment.level
      next_level = (
        Level.objects.filter(hierarchy__gt=current_level.hierarchy)
        .order_by('hierarchy')
        .first()
      )
    else:
      current_level = None
      next_level = Level.objects.order_by('hierarchy').first()

    return current_level, next_level

class Level(models.Model):
  code = models.CharField(max_length=4)
  description = models.CharField(max_length=128)
  study = models.SmallIntegerField()
  hierarchy = models.SmallIntegerField()
  
  def __str__(self):
    return self.code

class Prompt(ImageModel):
  user = models.ForeignKey('website.User', on_delete=models.CASCADE, related_name="prompts")
  language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="prompts")
  public = models.BooleanField(default=False)
  title = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255, unique=True, blank=True)
  content = models.TextField()
  image = models.CharField(max_length=255)
  level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="prompts")

  def save(self, *args, **kwargs):
    if not self.slug:
      # Initial slug generation
      self.slug = slugify(self.title)

      # Ensure uniqueness
      original_slug = self.slug
      queryset = Prompt.objects.filter(slug=self.slug).exists()
      counter = 1

      while queryset:
        self.slug = f"{original_slug}-{counter}"
        queryset = Prompt.objects.filter(slug=self.slug).exists()
        counter += 1

    super().save(*args, **kwargs)
  
  def __str__(self):
    return self.title

  def get_absolute_url(self): 
    return reverse("prompt_detail", kwargs={"slug": self.slug})

class Page(ImageModel):
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  content = HTMLField()
  image = models.CharField(max_length=255, null=True, blank=True)
  video = models.CharField(max_length=255, null=True, blank=True)


  def __str__(self):
    return self.title

class Post(ImageModel):
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  content = HTMLField()
  image = models.CharField(max_length=255, null=True, blank=True)
  video = models.CharField(max_length=255, null=True, blank=True)

  def __str__(self):
    return self.title

  def get_absolute_url(self): 
    return reverse("post_detail", kwargs={"slug": self.slug})

class TimeLog(BaseModel):
  user = models.ForeignKey('website.User', on_delete=models.CASCADE, related_name="time_logs")  
  date = models.DateTimeField()
  activity = models.CharField(max_length=128)
  duration = models.SmallIntegerField()
  
  def __str__(self):
    return self.activity

class Attainment(BaseModel):
  user = models.ForeignKey('website.User', on_delete=models.CASCADE, related_name="attainments")
  level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="attainments")
  language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="attainments")

  def __str__(self):
    return self.user.username + ' : ' + self.level.code

class Word(models.Model):
  word = models.CharField(max_length=100, unique=True)
  language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="words")
  part_of_speech = models.CharField(max_length=50)

  def __str__(self):
    return self.word

class TabooWord(models.Model):
  target_word = models.ForeignKey(Word, related_name='taboo_for', on_delete=models.CASCADE)
  taboo_word = models.ForeignKey(Word, related_name='is_taboo_word', on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.taboo_word.word} (taboo for {self.target_word.word})"

class TabooSet(models.Model):
  name = models.CharField(max_length=100)
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taboo_sets")
  language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="taboo_sets")

  def __str__(self):
    return f"{self.name} ({self.owner.username}, {self.language.name})"

class TabooCard(models.Model):
  taboo_set = models.ForeignKey(TabooSet, on_delete=models.CASCADE, related_name="cards")
  target = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="taboo_cards")

  def __str__(self):
    return f"{self.target.word} (Set: {self.taboo_set.name})"

class TabooCardTabooWord(models.Model):
  card = models.ForeignKey(TabooCard, on_delete=models.CASCADE, related_name="taboo_links")
  taboo_word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="as_taboo")

  class Meta:
    unique_together = ("card", "taboo_word")

  def __str__(self):
    return f"{self.taboo_word.word} (taboo for {self.card.target.word})"
