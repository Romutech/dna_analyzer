# Generated by Django 3.0.4 on 2020-06-20 21:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', models.TextField(null=True)),
                ('file_path', models.FileField(null=True, upload_to='')),
                ('note', models.TextField(null=True)),
                ('nb_bases', models.IntegerField(null=True)),
                ('nb_a', models.IntegerField(null=True)),
                ('nb_c', models.IntegerField(null=True)),
                ('nb_g', models.IntegerField(null=True)),
                ('nb_t', models.IntegerField(null=True)),
                ('percentage_a', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('percentage_c', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('percentage_g', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('percentage_t', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('percentage_gc', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('percentage_at', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('ratio_g_c_graph_data', models.TextField(null=True)),
                ('dna_walk_graph_data', models.TextField(null=True)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Date de création')),
            ],
        ),
        migrations.DeleteModel(
            name='Dna',
        ),
    ]