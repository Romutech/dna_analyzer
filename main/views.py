from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import DnaForm
from .models import Dna
from django.conf import settings
from tkinter import Tk
from collections import Counter
from .models import *


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


def genome_list(request):
    dnas = Dna.objects.all()
    return render(request, 'main/genome_list.html', locals())


def show(request, id):
    dna = get_object_or_404(Dna, id=id)
    return render(request, 'main/show.html', locals())


def analyze(request, id):
    dna = get_object_or_404(Dna, id=id)
    dna.analyse()
    return redirect('show', id)


def dna_walk(request, id):
    dna = get_object_or_404(Dna, id=id)
    return render(request, 'main/show.html', locals())


# def dna_walk(request, id):
#     dna = get_object_or_404(Dna, id=id)
#
#     graph = Graph()
#     genome = Genome(dna.file)
#     data = genome.data_rocessing()
#     graph.set_dna_sequence(genome)
#     graph.set_data(data)
#     graph.dna_walk_graph()
#     graph.show_statistics()
#     # graph.ratio_frequency_gc()
#
#     return render(request, 'main/show.html', locals())
#
#
# class Graph():
#     def __init__(self):
#         turtle.title("DNA analyzer")
#         turtle.speed(0)
#         turtle.shape('blank')
#         self.screen_size()
#         self.position_x = self.position_y = 0
#         self.distance = self.incrementation = 1
#
#     def set_data(self, data):
#         self.data = data
#
#     def set_dna_sequence(self, dna_sequence):
#         self.dna_sequence = str(dna_sequence)
#
#     def screen_size(self):
#         self.tk = Tk()
#         self.screenheight = self.tk.winfo_screenheight() - 50
#         self.screenwidth = self.tk.winfo_screenwidth()
#         turtle.setup(self.screenwidth, self.screenheight)
#         self.tk.destroy()
#
#     def get_distance(self):
#         distance = 1
#         if self.data['nb_bases'] < 1000:
#             distance = (self.screenheight / self.data['nb_bases']) * (
#                     self.size_window / ((self.data['nb_bases'] / 1000)) / 5)
#         elif self.data['nb_bases'] > 1000 and self.data['nb_bases'] <= 10000:
#             distance = (self.screenheight / self.data['nb_bases']) * (
#                     self.size_window / ((self.data['nb_bases'] / 20000)) / 5)
#         elif self.data['nb_bases'] > 10000 and self.data['nb_bases'] <= 1000000:
#             distance = (self.screenheight / self.data['nb_bases']) * (
#                     self.size_window / ((self.data['nb_bases'] / 80000)) / 5)
#         elif self.data['nb_bases'] > 1000000 and self.data['nb_bases'] <= 1000000000:
#             distance = (self.screenheight / self.data['nb_bases']) * (
#                     self.size_window / ((self.data['nb_bases'] / 90000)) / 5)
#         if self.data['nb_bases'] > 1000000000:
#             distance = (self.screenheight / self.data['nb_bases']) * (
#                     self.size_window / ((self.data['nb_bases'] / 90000)) / 5)
#         return distance
#
#     def dna_walk_graph_configuration(self):
#         turtle.pensize(1)
#         self.show_graphic_title()
#         self.size_window = int(self.data['nb_bases'] / 1000)
#         result = self.data['nb_t'] - self.data['nb_a']
#         self.distance = self.get_distance()
#         shift = result * self.distance
#         self.position_y = (shift / 2)
#         result = self.data['nb_g'] - self.data['nb_c']
#         shift = result * self.distance
#         self.position_x = shift / 2
#         self.position_y = self.position_y + 120
#         turtle.up()
#         turtle.goto(self.position_x, (self.position_y))
#         turtle.down()
#
#     def dna_walk_graph(self):
#         j = 0
#         turtle.clear()
#         self.dna_walk_legend()
#         self.dna_walk_graph_configuration()
#
#         if self.data['nb_bases'] > 1000000000:
#             distance = (self.screenheight / self.data['nb_bases']) * (
#                     self.size_window / ((self.data['nb_bases'] / (15000000))) / 5)
#
#         while j < len(self.dna_sequence):
#             i = 0
#             if i >= 50:
#                 break
#             while i < self.size_window and j < len(self.dna_sequence):
#                 if 'a' == str(self.dna_sequence[j]).lower():
#                     self.position_y += self.distance
#                 elif 'c' == str(self.dna_sequence[j]).lower():
#                     self.position_x += self.distance
#                 elif 'g' == str(self.dna_sequence[j]).lower():
#                     self.position_x -= self.distance
#                 elif 't' == str(self.dna_sequence[j]).lower():
#                     self.position_y -= self.distance
#                 j += self.incrementation
#                 i += self.incrementation
#
#             turtle.goto(self.position_x, self.position_y)
#         turtle.shape('blank')
#         ts = turtle.getscreen()
#         ts.getcanvas().postscript(file="dna_walk.eps")
#
#         from PIL import Image
#
#         TARGET_BOUNDS = (2048, 2048)
#         pic = Image.open('dna_walk.eps')
#         pic.load(scale=8)
#         if pic.mode in ('P', '1'):
#             pic = pic.convert("RGB")
#         ratio = min(TARGET_BOUNDS[0] / pic.size[0],
#                     TARGET_BOUNDS[1] / pic.size[1])
#         new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))
#         pic = pic.resize(new_size, Image.ANTIALIAS)
#         pic.save("dna_walk.png")
#
#     def ratio_frequency_gc(self):
#         j = nb_c = nb_g = 0
#         self.dna_walk_graph_configuration()
#         turtle.up()
#         position_x = -(self.screenwidth / 2 - 250)
#         position_y = -(self.screenheight / 2 - 120)
#         incrementation = int((self.screenwidth - 300) / 1000)
#         turtle.goto(-100, position_y + 100)
#         turtle.write("GC ratio frequency", font=("Arial", 17, "bold"))
#         font_size = 8
#         graduation = 1
#         ladder = 0.25
#         delta = 70
#         turtle.goto(position_x - 25, position_y + delta)
#
#         while True:
#             turtle.write(str(graduation), font=("Arial", font_size))
#             if graduation == -1:
#                 break
#             turtle.pensize(2)
#             delta += 5
#             turtle.goto(position_x - 5, position_y + delta)
#             turtle.down()
#             turtle.goto(position_x, position_y + delta)
#             delta -= 18.75
#             turtle.goto(position_x, position_y + delta)
#             delta -= 5
#             turtle.up()
#             turtle.goto(position_x - 25, position_y + delta)
#             turtle.pensize(1)
#             graduation -= ladder
#
#         turtle.goto(position_x - 5, position_y - 75)
#         turtle.down()
#         turtle.goto(position_x, position_y - 75)
#         turtle.goto(position_x, position_y)
#         turtle.pensize(3)
#         turtle.pencolor("red")
#         turtle.goto((self.screenwidth / 2 + 200), position_y)
#         turtle.up()
#         turtle.goto(position_x, position_y)
#         turtle.down()
#         turtle.pensize(1)
#         turtle.pencolor("black")
#
#         while j < len(self.dna_sequence):
#             i = 0
#             while i < self.size_window and j < len(self.dna_sequence):
#                 if 'g' == str(self.dna_sequence[j]).lower():
#                     nb_g += 1
#                 elif 'c' == str(self.dna_sequence[j]).lower():
#                     nb_c += 1
#
#                 j += self.incrementation
#                 i += self.incrementation
#
#             if 0 == (nb_g - nb_c) or 0 == (nb_g + nb_c):
#                 ratio_g_c = 0
#             else:
#                 ratio_g_c = (nb_g - nb_c) / (nb_g + nb_c)
#             position_x += incrementation
#             turtle.goto(position_x, (position_y + (75 * ratio_g_c)))
#             nb_c = nb_g = 0
#
#     def show_graphic_title(self):
#         turtle.up()
#         turtle.home()
#         turtle.goto(-100, (self.screenheight / 2) - 50)
#         display_analysis_results.show_title()
#         turtle.home()
#
#     def dna_walk_legend(self):
#         turtle.pensize(3)
#         position_x = self.screenwidth / 2.1
#         position_y = (self.screenheight / 2) / 10
#         turtle.up()
#         turtle.goto((position_x + 10), (position_y - 7))
#         turtle.write("C", font=("Arial", 15, "bold"))
#         turtle.goto(position_x, position_y)
#         turtle.down()
#         turtle.goto((position_x - 50), position_y)
#         turtle.up()
#         turtle.goto((position_x - 70), (position_y - 7))
#         turtle.write("G", font=("Arial", 15, "bold"))
#         turtle.goto((position_x - 28), (position_y + 35))
#         turtle.write("A", font=("Arial", 15, "bold"))
#         turtle.goto((position_x - 25), (position_y + 25))
#         turtle.down()
#         turtle.goto((position_x - 25), (position_y - 25))
#         turtle.up()
#         turtle.goto((position_x - 28), (position_y - 50))
#         turtle.write("T", font=("Arial", 15, "bold"))
#
#
# class display_analysis_results():
#     def show_title():
#         turtle.write("DNA walk graphic", font=("Arial", 17, "bold"))
#
#     def show(data):
#         turtle.write("\nThis genome is made up of " + str(data['nb_bases']) + " bases.\n\nThere are " + str(
#             data['nb_a']) + " bases which are adenine, \nor " + str(
#             round(data['percentage_a'], 2)) + "% of the sequence.\n\nThere are " + str(
#             data['nb_c']) + " bases which are cytosine,\n or " + str(
#             round(data['percentage_c'], 2)) + "% of the sequence.\n\nThere are " + str(
#             data['nb_g']) + " bases which are guanine, \nor " + str(
#             round(data['percentage_g'], 2)) + "% of the sequence.\n\nThere are " + str(
#             data['nb_t']) + " bases which are thymine, \nor " + str(
#             round(data['percentage_t'], 2)) + "% of the sequence.\n\nContent in GC : " + str(
#             round(data['percentage_gc'], 2)) + "%\nContent in AT : " + str(round(data['percentage_at'], 2)) + "%\n",
#                      font=("Arial", 12, "normal"))
#
#
# class Genome:
#     def __init__(self, sequence):
#         self.sequence = str(sequence).lower()
#         self.data = {}
#         turtle.shape('blank')
#
#     def __str__(self):
#         return self.sequence
#
#     def base_number_in_sequence(self, occurrences):
#         return occurrences['a'] + occurrences['c'] + occurrences['g'] + occurrences['t']
#
#     def number_nucleotides(self):
#         occurrences = Counter(self.sequence)
#         turtle.clear()
#         turtle.write("Detection of the number of bases contained in the genome!", font=("Arial", 18, "normal"))
#         self.data['nb_bases'] = self.base_number_in_sequence(occurrences)
#         self.data['nb_a'] = occurrences['a']
#         self.data['nb_c'] = occurrences['c']
#         self.data['nb_g'] = occurrences['g']
#         self.data['nb_t'] = occurrences['t']
#
#     def percentage_nucleotide(self):
#         self.data['percentage_a'] = (100 / self.data['nb_bases']) * self.data['nb_a']
#         self.data['percentage_c'] = (100 / self.data['nb_bases']) * self.data['nb_c']
#         self.data['percentage_g'] = (100 / self.data['nb_bases']) * self.data['nb_g']
#         self.data['percentage_t'] = (100 / self.data['nb_bases']) * self.data['nb_t']
#
#     def percentage_GC_AT(self):
#         self.data['percentage_gc'] = self.data['percentage_a'] + self.data['percentage_t']
#         self.data['percentage_at'] = self.data['percentage_g'] + self.data['percentage_c']
#
#     def data_rocessing(self):
#         turtle.clear()
#         turtle.home()
#         turtle.goto(-150, 0)
#         turtle.write("Data processing in progress!", font=("Arial", 18, "normal"))
#         self.number_nucleotides()
#         self.percentage_nucleotide()
#         self.percentage_GC_AT()
#         turtle.clear()
#         turtle.write("Data processing finished!", font=("Arial", 18, "normal"))
#         return self.data
