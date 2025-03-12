from django.db import models
from django.conf import settings
from tinymce.models import HTMLField

class BaseModel(models.Model):
  image = models.CharField(max_length=255)

  @property
  def image_url(self):
      return f"{settings.STORAGE_ROOT_URL}{self.image}"

  class Meta:
      abstract = True 

class Prompt(BaseModel):
  title = models.CharField(max_length=255)
  content = models.TextField()
  image = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title

class Page(BaseModel):
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  content = HTMLField()
  image = models.CharField(max_length=255, null=True, blank=True)
  video = models.CharField(max_length=255, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title

class Post(BaseModel):
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  content = HTMLField()
  image = models.CharField(max_length=255, null=True, blank=True)
  video = models.CharField(max_length=255, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title
