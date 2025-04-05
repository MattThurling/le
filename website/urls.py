from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('synful/', views.synful, name='synful'),
  path('prompts/', views.prompt_list, name='prompt_list'),
  path('prompts/<slug:slug>/', views.prompt_detail, name='prompt_detail'),
  path('pages/', views.page_list, name='page_list'),
  path('posts/', views.post_list, name='post_list'),
  path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
  path('progress/', views.ProgressView.as_view(), name='progress'),
  path('submit-timelog/', views.SubmitTimeLogView.as_view(), name='submit_timelog'),
  path('register/', views.register_view, name='register'),
  path('login/', views.CustomLoginView.as_view(), name='login'),

]
