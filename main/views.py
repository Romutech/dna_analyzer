from django.shortcuts import render

from graphic_interface import display_analysis_results
from genome import Genome
from graph import Graph

import turtle

def main():   
    loop = True
    while(loop):
        choice = int(input('\nTapez 1 pour analyser la sequence ADN du COVID-19\nTapez 2 pour analyser le genome de votre choix\nType 1 to analyze the COVID-19 DNA sequence\nType 2 to analyze the genome of your choice : '))
        if 1 == choice:
            file_name = 'isolate_wuhan-hu-1_complete_genome_covid-19.fna'
            loop = False
        elif 2 == choice:
            file_name = input('\nSaisissez le nom du fichier contenant la sequence genômique que vous avez placé dans le dossier << data >> du projet\nEnter the name of the file containing the genomic sequence that you placed in << data >> folder of the project : ')
            loop = False
        else :
           print('Choix incorrecte !\nWrong choice! ')
   
    graph = Graph()
    genome = Genome(file_name)
    data = genome.data_rocessing()
    graph.set_dna_sequence(genome)
    graph.set_data(data)
    graph.dna_walk_graph()
    graph.show_statistics()
    graph.ratio_frequency_gc()
   
    input("Press enter to stop the program !")
