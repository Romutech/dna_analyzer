# Generated by Django 3.0.4 on 2020-05-28 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_dna_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dna',
            name='file',
            field=models.TextField(null=True),
        ),
    ]