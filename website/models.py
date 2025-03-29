from django.db import models
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

class Prompt(ImageModel):
  title = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255, unique=True, blank=True)
  content = models.TextField()
  image = models.CharField(max_length=255)
  # Temporary hack for demo purposes. To be replaced with proper reference to user and organisation
  organisation = models.CharField(max_length=255, null=True,blank=True)
  level = models.CharField(max_length=8, null=True,blank=True)

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
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="time_logs")  
  date = models.DateTimeField()
  activity = models.CharField(max_length=128)
  duration = models.SmallIntegerField()
  
  def __str__(self):
    return self.activity

class Level(models.Model):
  code = models.CharField(max_length=4)
  description = models.CharField(max_length=128)
  study = models.SmallIntegerField()
  hierarchy = models.SmallIntegerField()
  
  def __str__(self):
    return self.code

class Attainment(BaseModel):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attainments")
  level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="attainments")

  def __str__(self):
    return self.user.username + ' : ' + self.level.code

# Simple method on User model
def get_attainments(self):
  return self.attainments.select_related('level').all()

# Attach it directly to the User model
User.add_to_class("get_attainments", get_attainments)

def get_current_and_next_level(self):
  # Get user's most recent attainment
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
    next_level = Level.objects.order_by('level').first()

  return current_level, next_level

# Attach directly to User
User.add_to_class("get_current_and_next_level", get_current_and_next_level)

