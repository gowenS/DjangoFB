from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('performcleanup', views.performCleanup, name='performcleanup'),
]