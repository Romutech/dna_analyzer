from django import forms
from .models import Sequence

class SequenceForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields = ('title', 'file_path', 'note',)


    def save(self):
        sequence = super().save()
        with open('media/' + str(sequence.file_path), 'r') as genome_file:
             genome_file.readline()
             sequence.file = genome_file.read()
             sequence.save()
        return sequence