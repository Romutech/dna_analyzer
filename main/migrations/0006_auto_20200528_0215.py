# Generated by Django 3.0.4 on 2020-05-28 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200528_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dna',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
