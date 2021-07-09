from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='user_home'),
    path('', include('django.contrib.auth.urls')),
]