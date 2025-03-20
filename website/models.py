from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from tinymce.models import HTMLField
from django.urls import reverse

class BaseModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  @property
  def image_url(self):
    return f"{settings.STORAGE_ROOT_URL}{self.image}"

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
  content = models.TextField()
  image = models.CharField(max_length=255)
  # Temporary hack for demo purposes. To be replaced with proper reference to user and organisation
  organisation = models.CharField(max_length=255, null=True,blank=True)
  level = models.CharField(max_length=8, null=True,blank=True)
  
  def __str__(self):
    return self.title

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

