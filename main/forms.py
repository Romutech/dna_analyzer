from django import forms
from .models import Dna

class DnaForm(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()