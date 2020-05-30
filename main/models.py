from django.db import models

class Dna(models.Model):
    title = models.TextField(max_length=50)
    file = models.TextField(null=True)
    file_path = models.FileField()
