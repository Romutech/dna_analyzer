
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import DnaForm
from .models import Dna
from django.conf import settings


def index(request):
    if request.method == 'POST':
        form = DnaForm(request.POST, request.FILES)
        if form.is_valid():
            dna = Dna()
            dna.title = form.cleaned_data['title']
            dna.file_path = form.cleaned_data['file']
            dna.save()
            with open('media/' + str(dna.file_path), 'r') as genome_file:
                genome_file.readline()
                dna.file = genome_file.read()
                dna.save()
            render(request, 'main/index.html', locals())
    else:
        form = DnaForm()
    return render(request, 'main/index.html', locals())

def show(request, id):
    dna = get_object_or_404(Dna, id=id)
    return render(request, 'main/show.html', locals())


# from graphic_interface import display_analysis_results
# from genome import Genome
# from graph import Graph
#
# import turtle
#
# def main():
#     loop = True
#     while(loop):
#         choice = int(input('\nTapez 1 pour analyser la sequence ADN du COVID-19\nTapez 2 pour analyser le genome de votre choix\nType 1 to analyze the COVID-19 DNA sequence\nType 2 to analyze the genome of your choice : '))
#         if 1 == choice:
#             file_name = 'isolate_wuhan-hu-1_complete_genome_covid-19.fna'
#             loop = False
#         elif 2 == choice:
#             file_name = input('\nSaisissez le nom du fichier contenant la sequence genômique que vous avez placé dans le dossier << data >> du projet\nEnter the name of the file containing the genomic sequence that you placed in << data >> folder of the project : ')
#             loop = False
#         else :
#            print('Choix incorrecte !\nWrong choice! ')
#
#     graph = Graph()
#     genome = Genome(file_name)
#     data = genome.data_rocessing()
#     graph.set_dna_sequence(genome)
#     graph.set_data(data)
#     graph.dna_walk_graph()
#     graph.show_statistics()
#     graph.ratio_frequency_gc()
#
#     input("Press enter to stop the program !")

    #interface import turtle

    # def show_title():
        # turtle.write("DNA walk graphic", font=("Arial", 17, "bold"))
    # def show(data):
        # turtle.write("\nThis genome is made up of " + str(data['nb_bases']) + " bases.\n\nThere are " + str(data['nb_a']) + " bases which are adenine, \nor " + str(round(data['percentage_a'], 2)) + "% of the sequence.\n\nThere are " + str(data['nb_c']) + " bases which are cytosine,\n or " + str(round(data['percentage_c'], 2)) + "% of the sequence.\n\nThere are " + str(data['nb_g']) + " bases which are guanine, \nor " + str(round(data['percentage_g'], 2)) + "% of the sequence.\n\nThere are " + str(data['nb_t']) + " bases which are thymine, \nor " + str(round(data['percentage_t'], 2)) + "% of the sequence.\n\nContent in GC : " + str(round(data['percentage_gc'], 2)) + "%\nContent in AT : " + str(round(data['percentage_at'], 2)) + "%\n", font=("Arial", 12, "normal"))