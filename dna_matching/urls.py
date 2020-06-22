from django.urls import path
from . import views

urlpatterns = [
    path('matching', views.matching, name="matching"),
]
