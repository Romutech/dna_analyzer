# Generated by Django 3.0.4 on 2020-05-28 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dna',
            name='file',
            field=models.FileField(upload_to='dnas'),
        ),
    ]
