from django.shortcuts import render, redirect, get_object_or_404
from .forms import SequenceForm
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage

from django.shortcuts import render
from matplotlib import pyplot as plt
import io
import urllib, base64
import matplotlib
matplotlib.use('Agg')

def home(request):
    plt.plot(range(10))
    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'main/home.html',{'data':uri})


def index(request, page=1):
    sequences = Sequence.objects.order_by('-date')
    paginator = Paginator(sequences, 2, 1)
    try:
        sequences = paginator.page(page)
    except EmptyPage:
        sequences = paginator.page(paginator.num_pages)

    return render(request, 'main/index.html', locals())


def create(request):
    if request.method == 'POST':
        form = SequenceForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect('read', form.save().id)
    form = SequenceForm()
    return render(request, 'main/sequence_form.html', locals())


def read(request, id):
    sequence = get_object_or_404(Sequence, id=id)
    if sequence.nb_bases is not None:
        sequence.nb_bases = int(sequence.nb_bases)
    return render(request, 'main/read.html', locals())


def update(request, id):
    sequence = get_object_or_404(Sequence, id=id)
    if request.method == 'POST':
        form = SequenceForm(request.POST, request.FILES, instance=sequence)
        if form.is_valid():
            form.save()
            return redirect('read', id)
    else:
        form = SequenceForm(instance=sequence)
    return render(request, 'main/sequence_form.html', locals())


def delete(request, id):
    sequence = get_object_or_404(Sequence, id=id)
    sequence.delete()
    messages.add_message(request, messages.SUCCESS, 'La séquence ADN a bien été supprimée !')
    return redirect('index')


def analyze(request, id):
    sequence = get_object_or_404(Sequence, id=id)
    sequence.analyse()
    return redirect('read', id)

