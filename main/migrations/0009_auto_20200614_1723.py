# Generated by Django 3.0.4 on 2020-06-14 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200614_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dna',
            name='percentage_a',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]