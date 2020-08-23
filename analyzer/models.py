from django.db import models
from django.utils import timezone
from matplotlib import pyplot as plt
import matplotlib
from collections import Counter
import urllib, base64
import io
from django.contrib.auth.models import User
matplotlib.use('Agg')


class Sequence(models.Model):
    def analyze(self, json_data):
        self.number_nucleotides(json_data)
        self.percentage_nucleotide(json_data)
        self.percentage_GC_AT(json_data)

        return json_data


    def number_nucleotides(self, json_data):
        occurrences = Counter(json_data['file'].lower())
        json_data['nb_bases'] = occurrences['a'] + occurrences['c'] + occurrences['g'] + occurrences['t']
        json_data['nb_a'] = occurrences['a']
        json_data['nb_c'] = occurrences['c']
        json_data['nb_g'] = occurrences['g']
        json_data['nb_t'] = occurrences['t']

        return json_data


    def percentage_nucleotide(self, json_data):
        json_data['percentage_a'] = round((100 / json_data['nb_bases']) * json_data['nb_a'], 2)
        json_data['percentage_c'] = round((100 / json_data['nb_bases']) * json_data['nb_c'], 2)
        json_data['percentage_g'] = round((100 / json_data['nb_bases']) * json_data['nb_g'], 2)
        json_data['percentage_t'] = round((100 / json_data['nb_bases']) * json_data['nb_t'], 2)

        return json_data


    def percentage_GC_AT(self, json_data):
        json_data['percentage_gc'] = round(json_data['percentage_g'] + json_data['percentage_c'], 2)
        json_data['percentage_at'] = round(json_data['percentage_a'] + json_data['percentage_t'], 2)

        return json_data


    def graph_image_generation(self, plt):
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=500)
        buf.seek(0)
        string = base64.b64encode(buf.read())
        plt.close(fig)
        return urllib.parse.quote(string)


    def dna_walk_graph(self, json_data):
        abscissa = []
        ordinate = []
        x = y = 0
        for nucleotide in json_data['file']:
            if 'a' == nucleotide.lower():
                y += 1
            elif 'c' == nucleotide.lower():
                x += 1
            elif 'g' == nucleotide.lower():
                x -= 1
            elif 't' == nucleotide.lower():
                y -= 1
            ordinate.append(y)
            abscissa.append(x)
        plt.figure(figsize=(10, 10))
        plt.plot(abscissa, ordinate, "black", linewidth=0.7, )
        plt.grid(True)
        json_data['dna_walk_graph_data'] = self.graph_image_generation(plt)


    def ratio_g_c_graph(self, json_data):
        nb_windows = 1000
        abscissa = []
        size_window = 10
        if nb_windows * size_window < json_data['nb_bases'] :
            size_window = json_data['nb_bases'] // nb_windows
            nb_windows = self.determine_number_of_windows(nb_windows, size_window, json_data)
        else:
            nb_windows = json_data['nb_bases'] // size_window
        plt.figure(figsize=(11.5, 4))
        plt.gca().set_xlabel('Nombre de fenêtres (' + str(size_window) + ' nucléotides par fenêtre)')
        ordinate = self.determine_ration_c_g(nb_windows, size_window, json_data)
        [abscissa.append(nb) for nb in range(len(ordinate))]
        plt.plot(abscissa, ordinate, linewidth=1)
        plt.plot(abscissa, [0 for _ in range(len(ordinate))], "r")
        plt.axis([0, len(ordinate), -1, 1])
        plt.grid(True)
        json_data['ratio_g_c_graph_data'] = self.graph_image_generation(plt)


    def determine_number_of_windows(self, nb_windows, size_window, json_data):
        rest = json_data['nb_bases'] % nb_windows
        if rest > size_window:
            while rest > size_window:
                nb_windows = nb_windows + (rest // size_window)
                rest = rest % size_window
        if rest > 0:
            nb_windows += 1
        return nb_windows


    def determine_ration_c_g(self, nb_windows, size_window, json_data):
        number_windows_incremented = number_window_size_incremented = index_file = nb_g = nb_c = 0
        ratios = []
        while number_windows_incremented < nb_windows:
            while number_window_size_incremented < size_window and index_file < json_data['nb_bases']:
                if 'g' == str(json_data['file'][index_file]).lower():
                    nb_g += 1
                elif 'c' == str(json_data['file'][index_file]).lower():
                    nb_c += 1
                number_window_size_incremented += 1
                index_file += 1
            number_windows_incremented += 1
            if 0 == (nb_g + nb_c):
                ratio_g_c = 0
            else:
                ratio_g_c = (nb_g - nb_c) / (nb_g + nb_c)
            ratios.append(ratio_g_c)
            number_window_size_incremented = 0
            nb_g = nb_c = 0
        return ratios
