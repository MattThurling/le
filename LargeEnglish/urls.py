from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from website.sitemaps import StaticViewSitemap, PostSitemap

sitemaps = {
    'static': StaticViewSitemap(),
    'Post': PostSitemap(),

}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('', include('website.api.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]

