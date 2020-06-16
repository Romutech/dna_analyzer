from django.shortcuts import render, redirect, get_object_or_404
from .forms import DnaForm
from .models import *
from django.contrib import messages


def index(request):
    dnas = Dna.objects.order_by('-date')
    return render(request, 'main/index.html', locals())


def create(request):
    if request.method == 'POST':
        form = DnaForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect('read', form.save().id)
    form = DnaForm()
    return render(request, 'main/dna_form.html', locals())


def read(request, id):
    dna = get_object_or_404(Dna, id=id)
    if dna.nb_bases is not None:
        dna.nb_bases = int(dna.nb_bases)
    return render(request, 'main/read.html', locals())


def update(request, id):
    dna = get_object_or_404(Dna, id=id)
    if request.method == 'POST':
        form = DnaForm(request.POST, request.FILES, instance=dna)
        if form.is_valid():
            form.save()
            print("test")
            return redirect('read', id)
    else:
        form = DnaForm(instance=dna)
    return render(request, 'main/dna_form.html', locals())


def delete(request, id):
    dna = get_object_or_404(Dna, id=id)
    dna.delete()
    messages.add_message(request, messages.SUCCESS, 'La séquence ADN a bien été supprimée !')
    return redirect('index')


def analyze(request, id):
    dna = get_object_or_404(Dna, id=id)
    dna.analyse()
    return redirect('read', id)
