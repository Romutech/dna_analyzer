from django.db import models
from django.utils import timezone
from matplotlib import pyplot as plt
import matplotlib
from collections import Counter
import urllib, base64
import io

matplotlib.use('Agg')

class Sequence(models.Model):
    title                = models.CharField(max_length=100, null=False)
    file                 = models.TextField(null=True)
    file_path            = models.FileField(null=True)
    note                 = models.TextField(null=True)
    nb_bases             = models.IntegerField(null=True)
    nb_a                 = models.IntegerField(null=True)
    nb_c                 = models.IntegerField(null=True)
    nb_g                 = models.IntegerField(null=True)
    nb_t                 = models.IntegerField(null=True)
    percentage_a         = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    percentage_c         = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    percentage_g         = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    percentage_t         = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    percentage_gc        = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    percentage_at        = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    ratio_g_c_graph_data = models.TextField(null=False)
    date                 = models.DateField(default=timezone.now, verbose_name="Date de création")


    def analyse(self):
        self.number_nucleotides()
        self.percentage_nucleotide()
        self.percentage_GC_AT()
        models.Model.save(self)
        return self


    def number_nucleotides(self):
        occurrences = Counter(self.file.lower())
        self.nb_bases = occurrences['a'] + occurrences['c'] + occurrences['g'] + occurrences['t']
        self.nb_a = occurrences['a']
        self.nb_c = occurrences['c']
        self.nb_g = occurrences['g']
        self.nb_t = occurrences['t']


    def percentage_nucleotide(self):
        self.percentage_a = (100 / self.nb_bases) * self.nb_a
        self.percentage_c = (100 / self.nb_bases) * self.nb_c
        self.percentage_g = (100 / self.nb_bases) * self.nb_g
        self.percentage_t = (100 / self.nb_bases) * self.nb_t


    def percentage_GC_AT(self):
        self.percentage_gc = self.percentage_a + self.percentage_t
        self.percentage_at = self.percentage_g + self.percentage_c


    def graph_image_generation(self, plt):
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=500)
        buf.seek(0)
        string = base64.b64encode(buf.read())
        self.ratio_g_c_graph_data = urllib.parse.quote(string)
        self.save()


    def ratio_g_c_graph(self):
        nb_windows = 1000
        abscissa = []
        size_window = 10
        if nb_windows < self.nb_bases:
            size_window = self.nb_bases // nb_windows
            nb_windows = self.determine_number_of_windows(nb_windows, size_window)
        plt.figure(figsize=(11.5, 4))
        plt.gca().set_xlabel('Nombre de fenêtres (' + str(size_window) + ' nucléotides par fenêtre)')
        ordinate = self.determine_ration_c_g(nb_windows, size_window)
        [abscissa.append(nb) for nb in range(len(ordinate))]
        plt.plot(abscissa, ordinate, linewidth=1)
        plt.plot(abscissa, [0 for _ in range(len(ordinate))], "r")
        plt.axis([0, len(ordinate), -1, 1])
        plt.grid(True)
        self.graph_image_generation(plt)


    def determine_number_of_windows(self, nb_windows, size_window):
        rest = self.nb_bases % nb_windows
        if rest > size_window:
            while rest > size_window:
                nb_windows = nb_windows + (rest // size_window)
                rest = rest % size_window
        if rest > 0:
            nb_windows += 1
        return nb_windows


    def determine_ration_c_g(self, nb_windows, size_window):
        number_windows_incremented = number_window_size_incremented = index_file = nb_g = nb_c = 0
        ratios = []
        while number_windows_incremented < nb_windows:
            while number_window_size_incremented < size_window and index_file < self.nb_bases:
                if 'g' == str(self.file[index_file]).lower():
                    nb_g += 1
                elif 'c' == str(self.file[index_file]).lower():
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
