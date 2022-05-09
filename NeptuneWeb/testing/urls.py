# Filew which stores all urls with the corrosponding templates for App "login"

from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('dashboard/', views.dashboard), 
    path('', views.testing),
    path('routes/', views.routes),
    path('users/', views.getUsers), 
    path('users/<str:pk>', views.getUser)
]

urlpatterns += staticfiles_urlpatterns()