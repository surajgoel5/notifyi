from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='jobs_home'),
    path('verify_key/', views.verify_key, name='verify_key'),
    path('job_request/', views.job_request, name='job_request'),
    path('disp_user_key/', views.disp_user_key, name='disp_user_key'),
    
]