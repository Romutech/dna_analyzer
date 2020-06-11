from django.db import models
from collections import Counter

from django.utils import timezone


class Dna(models.Model):
    """
        self.data['nb_bases']
        self.data['nb_a']
        self.data['nb_c']
        self.data['nb_g']
        self.data['nb_t']

    """
    title           = models.TextField(max_length=50)
    file            = models.TextField(null=True)
    file_path       = models.FileField()
    nb_bases        = models.TextField(max_length=50, null=True)
    nb_a            = models.TextField(max_length=50, null=True)
    nb_c            = models.TextField(max_length=50, null=True)
    nb_g            = models.TextField(max_length=50, null=True)
    nb_t            = models.TextField(max_length=50, null=True)
    percentage_a    = models.TextField(max_length=50, null=True)
    percentage_c    = models.TextField(max_length=50, null=True)
    percentage_g    = models.TextField(max_length=50, null=True)
    percentage_t    = models.TextField(max_length=50, null=True)
    percentage_gc   = models.TextField(max_length=50, null=True)
    percentage_at   = models.TextField(max_length=50, null=True)
    date            = models.DateField(default=timezone.now, verbose_name="Date de création")

    def dna_walk(self):
        pass


    def analyse(self):
        self.number_nucleotides()
        self.percentage_nucleotide()
        self.percentage_GC_AT()
        self.save()
        return self


    def number_nucleotides(self):
        occurrences = Counter(self.file)
        print(occurrences)
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