# Filew which stores all urls with the corrosponding templates for App "login"

from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.layout_test)
]

urlpatterns += staticfiles_urlpatterns()
