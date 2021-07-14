from django.urls import path, include
from django.contrib.auth import views as authviews
from . import views

urlpatterns = [
    path('', views.index, name='user_home'),
    path('login/', authviews.LoginView.as_view(), name='login'),
    path('logout/', authviews.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

]