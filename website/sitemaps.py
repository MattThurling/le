from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

class StaticViewSitemap(Sitemap):
  priority = 0.5
  changefreq = 'weekly'

  def items(self):
    return ['index']

  def location(self, item):
    return reverse(item)

class PostSitemap(Sitemap):

  priority = 0.8
  changefreq = 'daily'

  def items(self):
    return Post.objects.all()

  def lastmod(self, obj):
    return obj.updated_at

