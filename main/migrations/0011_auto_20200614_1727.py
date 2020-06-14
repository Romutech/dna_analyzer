# Generated by Django 3.0.4 on 2020-06-14 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200614_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dna',
            name='percentage_a',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='dna',
            name='percentage_at',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='dna',
            name='percentage_c',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='dna',
            name='percentage_g',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='dna',
            name='percentage_gc',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='dna',
            name='percentage_t',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
