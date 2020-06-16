from django.db import models
from collections import Counter

from django.utils import timezone


class Dna(models.Model):
    title           = models.CharField(max_length=100, null=False)
    file            = models.TextField(null=True)
    file_path       = models.FileField(null=True)
    note            = models.TextField(null=True)
    nb_bases        = models.IntegerField(null=True)
    nb_a            = models.IntegerField(null=True)
    nb_c            = models.IntegerField(null=True)
    nb_g            = models.IntegerField(null=True)
    nb_t            = models.IntegerField(null=True)
    percentage_a    = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    percentage_c    = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    percentage_g    = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    percentage_t    = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    percentage_gc   = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    percentage_at   = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    date            = models.DateField(default=timezone.now, verbose_name="Date de création")


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
