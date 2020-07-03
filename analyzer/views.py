from django.shortcuts import render, redirect, get_object_or_404
from .forms import SequenceForm
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage

def index(request, page=1):
    if not request.user.is_active:
        return redirect('user_login')
    sequences = Sequence.objects.filter(user=request.user.id)
    paginator = Paginator(sequences, 20, 5)
    try:
        sequences = paginator.page(page)
    except EmptyPage:
        sequences = paginator.page(paginator.num_pages)
    return render(request, 'analyzer/index.html', locals())


def create(request):
    if not request.user.is_active:
        return redirect('user_login')
    if request.method == 'POST':
        form = SequenceForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect('read', form.save(request.user.id).id)
    form = SequenceForm()
    return render(request, 'analyzer/sequence_form.html', locals())


def read(request, id):
    if not request.user.is_active:
        return redirect('user_login')
    sequence = get_object_or_404(Sequence, id=id, user=request.user.id)
    if sequence.nb_bases is not None:
        sequence.nb_bases = int(sequence.nb_bases)
    return render(request, 'analyzer/read.html', locals())


def update(request, id):
    if not request.user.is_active:
        return redirect('user_login')
    sequence = get_object_or_404(Sequence, id=id, user=request.user.id)
    if request.method == 'POST':
        form = SequenceForm(request.POST, request.FILES, instance=sequence)
        if form.is_valid():
            form.save(request.user.id)
            return redirect('read', id)
    else:
        form = SequenceForm(instance=sequence)
    return render(request, 'analyzer/sequence_form.html', locals())


def delete(request, id):
    if not request.user.is_active:
        return redirect('user_login')
    sequence = get_object_or_404(Sequence, id=id, user=request.user.id)
    sequence.delete()
    messages.add_message(request, messages.SUCCESS, 'La séquence ADN a bien été supprimée !')
    return redirect('index')


def analyze(request, id):
    if not request.user.is_active:
        return redirect('user_login')
    sequence = get_object_or_404(Sequence, id=id, user=request.user.id)
    sequence.analyze()
    sequence.ratio_g_c_graph()
    sequence.dna_walk_graph()
    return redirect('read', id)

