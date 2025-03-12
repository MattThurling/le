from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('prompts/', views.prompt_list, name='prompt_list'),
  path('pages/', views.page_list, name='page_list'),
  path('posts/', views.post_list, name='post_list'),
  path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
]
