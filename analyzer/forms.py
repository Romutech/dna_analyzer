from django import forms
from .models import Sequence

class SequenceForm(forms.Form):
    title = forms.CharField(max_length=100)
    file_path = forms.FileField(required= True)
    note = forms.CharField(widget=forms.Textarea)

class SequenceFormUpdate(forms.Form):
    title = forms.CharField(max_length=100)
    file_path = forms.FileField(required= False)
    note = forms.CharField(widget=forms.Textarea)