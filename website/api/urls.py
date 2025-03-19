from django.urls import path, include
from django.contrib.auth import views as auth_views

from rest_framework.routers import DefaultRouter
from .views import TimeLogViewSet

router = DefaultRouter()
router.register(r'timelogs', TimeLogViewSet, basename='timelog')

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
