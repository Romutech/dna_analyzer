from django.shortcuts import render, redirect, get_object_or_404
from .forms import DnaForm
from .models import *


def index(request):
    return render(request, 'main/index.html')


def create(request):
    if request.method == 'POST':
        form = DnaForm(request.POST, request.FILES)
        if form.is_valid():
            dna = Dna()
            dna.save(form)
            return redirect('show', dna.id)
    else:
        form = DnaForm()
    return render(request, 'main/create.html', locals())


def show(request, id):
    dna = get_object_or_404(Dna, id=id)
    if dna.nb_bases is not None:
        dna.nb_bases = int(dna.nb_bases)
    return render(request, 'main/show.html', locals())


def genome_list(request):
    dnas = Dna.objects.all()
    return render(request, 'main/genome_list.html', locals())


def analyze(request, id):
    dna = get_object_or_404(Dna, id=id)
    dna.analyse()
    return redirect('show', id)
