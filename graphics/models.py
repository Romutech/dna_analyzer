from django.db import models

import turtle
from tkinter import *
from graphic_interface import display_analysis_results

import cairosvg

class Graph():
    def __init__(self):
        turtle.title("DNA analyzer")
        turtle.speed(0)
        turtle.shape('blank')
        self.screen_size()
        self.position_x = self.position_y = 0
        self.distance = self.incrementation = 1


    def set_data(self, data):
        self.data = data


    def set_dna_sequence(self, dna_sequence):
        self.dna_sequence = str(dna_sequence)


    def screen_size(self):
        self.tk=Tk()
        self.screenheight = self.tk.winfo_screenheight() - 50
        self.screenwidth = self.tk.winfo_screenwidth()
        self.tk.destroy()
        turtle.setup(self.screenwidth, self.screenheight)


    def get_distance(self):
        distance = 1
        if self.data['nb_bases'] < 1000:
            distance = (self.screenheight / self.data['nb_bases'] ) * (self.size_window / ((self.data['nb_bases'] / 1000))/5)
        elif self.data['nb_bases'] > 1000 and self.data['nb_bases'] <= 10000:
            distance = (self.screenheight / self.data['nb_bases'] ) * (self.size_window / ((self.data['nb_bases'] / 20000))/5)
        elif self.data['nb_bases'] > 10000 and self.data['nb_bases'] <= 1000000:
            distance = (self.screenheight / self.data['nb_bases'] ) * (self.size_window / ((self.data['nb_bases'] / 80000))/5)
        elif self.data['nb_bases'] > 1000000 and self.data['nb_bases'] <= 1000000000:
            distance = (self.screenheight / self.data['nb_bases'] ) * (self.size_window / ((self.data['nb_bases'] / 90000))/5)
        if self.data['nb_bases'] > 1000000000:
            distance = (self.screenheight / self.data['nb_bases'] ) * (self.size_window / ((self.data['nb_bases'] / 90000))/5)
        return distance


    def dna_walk_graph_configuration (self): 
        turtle.pensize(1)
        self.show_graphic_title()
        self.size_window = int(self.data['nb_bases'] / 1000)
        result = self.data['nb_t'] - self.data['nb_a']
        self.distance = self.get_distance()
        shift = result * self.distance
        self.position_y = (shift / 2)
        result = self.data['nb_g'] - self.data['nb_c']
        shift = result * self.distance
        self.position_x = shift / 2
        self.position_y = self.position_y + 120
        turtle.up()
        turtle.goto(self.position_x, (self.position_y))
        turtle.down()

        
    def dna_walk_legend(self):
        turtle.pensize(3)
        position_x = self.screenwidth / 2.1
        position_y = (self.screenheight / 2) / 10
        turtle.up()
        turtle.goto((position_x + 10), (position_y - 7))
        turtle.write("C", font=("Arial", 15, "bold"))
        turtle.goto(position_x, position_y)
        turtle.down()
        turtle.goto((position_x - 50), position_y)
        turtle.up()
        turtle.goto((position_x - 70), (position_y - 7))
        turtle.write("G", font=("Arial", 15, "bold"))
        turtle.goto((position_x - 28), (position_y + 35))
        turtle.write("A", font=("Arial", 15, "bold"))
        turtle.goto((position_x - 25), (position_y + 25))
        turtle.down()
        turtle.goto((position_x - 25), (position_y - 25))
        turtle.up()
        turtle.goto((position_x - 28), (position_y - 50))
        turtle.write("T", font=("Arial", 15, "bold"))
  

    def dna_walk_graph(self):
        j = 0
        turtle.clear()
        self.dna_walk_legend()
        self.dna_walk_graph_configuration()

        if self.data['nb_bases'] > 1000000000:
            distance = (self.screenheight / self.data['nb_bases'] ) * (self.size_window / ((self.data['nb_bases'] / (15000000)))/5)
        
        while j < len(self.dna_sequence):
            i =0
            print(i)
            if i >= 50:
                break
            while i < self.size_window and j < len(self.dna_sequence):
                if 'a' == str(self.dna_sequence[j]).lower():
                    self.position_y += self.distance
                elif 'c' == str(self.dna_sequence[j]).lower():
                    self.position_x += self.distance
                elif 'g' == str(self.dna_sequence[j]).lower():
                    self.position_x -= self.distance
                elif 't' == str(self.dna_sequence[j]).lower():
                    self.position_y -= self.distance
                j += self.incrementation
                i += self.incrementation

            turtle.goto(self.position_x,self.position_y)
        turtle.shape('blank')
        ts = turtle.getscreen()
        ts.getcanvas().postscript(file="dna_walk.eps")


        from PIL import Image

        TARGET_BOUNDS = (2048, 2048)
        pic = Image.open('dna_walk.eps')
        pic.load(scale=8)
        if pic.mode in ('P', '1'):
            pic = pic.convert("RGB")
        ratio = min(TARGET_BOUNDS[0] / pic.size[0],
                    TARGET_BOUNDS[1] / pic.size[1])
        new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))
        pic = pic.resize(new_size, Image.ANTIALIAS)
        pic.save("dna_walk.png")



    def ratio_frequency_gc(self):
        j = nb_c = nb_g = 0
        self.dna_walk_graph_configuration()
        turtle.up()
        position_x = -(self.screenwidth / 2 - 250)
        position_y = -(self.screenheight / 2 - 120)
        incrementation = int((self.screenwidth - 300) / 1000) 
        turtle.goto(-100,  position_y + 100)
        turtle.write("GC ratio frequency", font=("Arial", 17, "bold"))
        font_size = 8
        graduation = 1
        ladder = 0.25
        delta = 70
        turtle.goto(position_x - 25, position_y + delta)

        while True:
            turtle.write(str(graduation), font=("Arial", font_size))
            if graduation == -1:
                break
            turtle.pensize(2)
            delta +=5
            turtle.goto(position_x - 5, position_y + delta)
            turtle.down()
            turtle.goto(position_x, position_y + delta)
            delta -= 18.75
            turtle.goto(position_x, position_y + delta)
            delta -= 5
            turtle.up()
            turtle.goto(position_x - 25, position_y + delta)
            turtle.pensize(1)
            graduation -= ladder
            

        turtle.goto(position_x - 5, position_y - 75)
        turtle.down()
        turtle.goto(position_x,  position_y - 75)
        turtle.goto(position_x,  position_y)
        turtle.pensize(3)
        turtle.pencolor("red")
        turtle.goto((self.screenwidth / 2 + 200) , position_y)
        turtle.up()
        turtle.goto(position_x, position_y)
        turtle.down()
        turtle.pensize(1)
        turtle.pencolor("black")
        
        
        while j < len(self.dna_sequence):
            i =0
            while i < self.size_window and j < len(self.dna_sequence):
                if 'g' == str(self.dna_sequence[j]).lower():
                    nb_g += 1
                elif 'c' == str(self.dna_sequence[j]).lower():
                    nb_c += 1
                
                j += self.incrementation
                i += self.incrementation

            if 0 == (nb_g - nb_c) or 0 == (nb_g + nb_c):
                ratio_g_c = 0
            else:
                ratio_g_c = (nb_g - nb_c) / (nb_g + nb_c)
            position_x += incrementation
            turtle.goto(position_x, (position_y + (75 * ratio_g_c)))
            nb_c = nb_g = 0


    def show_graphic_title(self):
        turtle.up()
        turtle.home()
        turtle.goto(-100, (self.screenheight / 2) -50) 
        display_analysis_results.show_title()
        turtle.home()


    def show_statistics(self):
        turtle.up()
        turtle.home()
        position_x = self.screenwidth / 2
        position_y = self.screenheight / 2

        turtle.goto(-position_x + 10, position_y - 300)
        display_analysis_results.show(self.data)


from graphic_interface import display_analysis_results
from genome import Genome
from graph import Graph

import turtle

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
    
