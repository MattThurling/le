from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post, Prompt

class StaticViewSitemap(Sitemap):
  priority = 0.5
  changefreq = 'weekly'

  def items(self):
    return ['index']

  def location(self, item):
    return reverse(item)

class PostSitemap(Sitemap):

  priority = 0.8
  changefreq = 'weekly'

  def items(self):
    return Post.objects.all()

  def lastmod(self, obj):
    return obj.updated_at

class PromptSitemap(Sitemap):

  priority = 0.8
  changefreq = 'daily'

  # Return only the English ones
  def items(self):
    return Prompt.objects.filter(organisation__isnull=True)

  def lastmod(self, obj):
    return obj.updated_at

