from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import SequenceForm
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
import requests
from django.conf import settings
import json

def index(request, page=1):
    # -----------------------------------------------
    resp = requests.get(settings.URL())

    sequences = resp.json()

    paginator = Paginator(sequences, 20, 5)
    try:
        sequences = paginator.page(page)
    except EmptyPage:
        sequences = paginator.page(paginator.num_pages)
    return render(request, 'analyzer/index.html', locals())


    # -----------------------------------------------

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
            # fichier = open('media/' + str(request.FILES['file_path'], 'wt')
            # fichier.write(
            #     "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \nPellentesque gravida erat ut lectus convallis auctor. \nFusce mollis sem id tellus auctor hendrerit.")
            # fichier.close()

            file = request.FILES['file_path']

            with open('media/' + str(request.FILES['file_path']) , 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)


            with open('media/' + str(request.FILES['file_path']), 'r') as genome_file:
                genome_file.readline()

                json_data = {
                    'title': request.POST['title'],
                    'file_path': str(request.FILES['file_path']),
                    'note': request.POST['note'],
                    'user_id': request.user.id,
                    'file': genome_file.read()
                }

            requests.post(settings.URL(), json=json_data)

            return redirect('index')
    form = SequenceForm()
    return render(request, 'analyzer/sequence_form.html', locals())


def read(request, id):
    # -----------------------------------------------

    resp = requests.get(settings.URL(id))

    sequence = resp.json()

    if sequence['nb_bases'] is not None:
        sequence.nb_bases = int(sequence.nb_bases)
    return render(request, 'analyzer/read.html', locals())

    # -----------------------------------------------

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

