from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('genome_list', views.genome_list, name="genome_list"),
    path('<id>', views.show, name="show"),
    path('dna/<id>', views.dna_walk, name="dna_wolk"),
    path('dna/<id>/analyze', views.analyze, name="analyze"),
]
