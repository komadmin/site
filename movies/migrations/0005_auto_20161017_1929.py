# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-17 19:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20161017_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='similarmovierel',
            name='similar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='linkto', to='movies.Movie'),
        ),
        migrations.AlterField(
            model_name='similarmovierel',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='linkfrom', to='movies.Movie'),
        ),
    ]