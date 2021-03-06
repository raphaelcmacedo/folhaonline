# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-12 14:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20161016_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContraCheque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercicio', models.IntegerField()),
                ('mes', models.IntegerField(blank=True)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=100, verbose_name='Numero')),
            ],
        ),
        migrations.CreateModel(
            name='Orgao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigla', models.CharField(max_length=20, verbose_name='Sigla')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('municipio', models.CharField(choices=[('001', 'Trajano de Moraes')], max_length=100, verbose_name='Nome')),
            ],
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.AddField(
            model_name='matricula',
            name='orgao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Orgao'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contracheque',
            name='matricula',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Matricula'),
        ),
    ]
