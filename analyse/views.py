from django.shortcuts import render, redirect, get_object_or_404
from .forms import SequenceForm
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage

def index(request, page=1):
    sequences = Sequence.objects.order_by('-id')
    paginator = Paginator(sequences, 20, 5)
    try:
        sequences = paginator.page(page)
    except EmptyPage:
        sequences = paginator.page(paginator.num_pages)
    return render(request, 'analyse/index.html', locals())


def create(request):
    if request.method == 'POST':
        form = SequenceForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect('read', form.save().id)
    form = SequenceForm()
    return render(request, 'analyse/sequence_form.html', locals())


def read(request, id):
    sequence = get_object_or_404(Sequence, id=id)
    if sequence.nb_bases is not None:
        sequence.nb_bases = int(sequence.nb_bases)
    return render(request, 'analyse/read.html', locals())


def update(request, id):
    sequence = get_object_or_404(Sequence, id=id)
    if request.method == 'POST':
        form = SequenceForm(request.POST, request.FILES, instance=sequence)
        if form.is_valid():
            form.save()
            return redirect('read', id)
    else:
        form = SequenceForm(instance=sequence)
    return render(request, 'analyse/sequence_form.html', locals())


def delete(request, id):
    sequence = get_object_or_404(Sequence, id=id)
    sequence.delete()
    messages.add_message(request, messages.SUCCESS, 'La séquence ADN a bien été supprimée !')
    return redirect('index')


def analyze(request, id):
    sequence = get_object_or_404(Sequence, id=id)
    sequence.analyse()
    sequence.ratio_g_c_graph()
    sequence.dna_walk_graph()
    return redirect('read', id)

