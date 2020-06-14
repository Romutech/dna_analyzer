from django import forms
from .models import Dna

class DnaForm(forms.ModelForm):
    class Meta:
        model = Dna
        fields = ('title', 'file_path', 'note',)


    def save(self):
        dna = super().save()
        with open('media/' + str(dna.file_path), 'r') as genome_file:
             genome_file.readline()
             dna.file = genome_file.read()
             dna.save()
        return dna