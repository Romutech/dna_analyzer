from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('page/<int:page>', views.index, name="index"),
    path('create', views.create, name="create"),
    path('<int:id>', views.read, name="read"),
    path('update/<int:id>', views.update, name="update"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('sequence/<int:id>/analyze', views.analyze, name="analyze"),
    ]
