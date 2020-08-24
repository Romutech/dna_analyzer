from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('page/<int:page>', views.index, name="index"),
    path('create', views.create, name="create"),
    path('<str:unique_id>', views.read, name="read"),
    path('update/<str:unique_id>', views.update, name="update"),
    path('delete/<str:unique_id>', views.delete, name="delete"),
    path('sequence/<str:unique_id>/analyze', views.analyze, name="analyze"),
]
