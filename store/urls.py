from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # This will handle the root URL
]