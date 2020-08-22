from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import SequenceForm, SequenceFormUpdate
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
import requests
from django.conf import settings
import json
import uuid

def index(request, page=1):
    if not request.user.is_active:
        return redirect('user_login')

    response = requests.get(settings.URL())
    sequences = response.json()
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
            file = request.FILES['file_path']

            with open('media/' + str(file) , 'wb+') as genome_file:
                for chunk in file.chunks():
                    genome_file.write(chunk)

            with open('media/' + str(file), 'r') as genome_file:
                genome_file.readline()
                file = genome_file.read()

            json_data = {
                'title': request.POST['title'],
                'file_path': str(request.FILES['file_path']),
                'note': request.POST['note'],
                'user_id': request.user.id,
                'file': file
            }

            requests.post(settings.URL(), json=json_data)
            response = requests.get(settings.URL())
            sequences = response.json()
            paginator = Paginator(sequences, 20, 5)

            try:
                sequences = paginator.page(1)
            except EmptyPage:
                sequences = paginator.page(paginator.num_pages)
            return render(request, 'analyzer/index.html', locals())
            return render(request, 'analyzer/read.html', locals())



    form = SequenceForm()
    return render(request, 'analyzer/sequence_form.html', locals())


def read(request, unique_id):
    response = requests.get(settings.URL(unique_id))

    sequence = response.json()

    if sequence['nb_bases'] is not None:
        sequence.nb_bases = int(sequence.nb_bases)
    return render(request, 'analyzer/read.html', locals())


def update(request, unique_id):
    if not request.user.is_active:
        return redirect('user_login')

    response = requests.get(settings.URL(unique_id))

    sequence = response.json()

    if request.method == 'POST':
        form = SequenceFormUpdate(request.POST, request.FILES)
        if form.is_valid():
            if 'file_path' in request.FILES:
                file = request.FILES['file_path']

                with open('media/' + str(file), 'wb+') as genome_file:
                    for chunk in file.chunks():
                        genome_file.write(chunk)

                with open('media/' + str(file), 'r') as genome_file:
                    genome_file.readline()
                    file = genome_file.read()

            json_data = {
                'title': request.POST['title'],
                'note': request.POST['note'],
                'user_id': request.user.id,
            }

            if 'file' in locals():
                json_data['file_path'] = str(request.FILES['file_path'])
                json_data['file'] = file

            requests.put(settings.URL(unique_id), json=json_data)

            return redirect('read', unique_id)
    else:
        form = SequenceFormUpdate(sequence)
    return render(request, 'analyzer/sequence_form.html', locals())


def delete(request, unique_id):
    if not request.user.is_active:
        return redirect('user_login')
    sequence = get_object_or_404(Sequence, id=unique_id, user=request.user.id)
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

