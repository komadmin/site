# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 21:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ActorID')),
                ('name', models.CharField(max_length=50, verbose_name='Actor Name')),
                ('profilepath', models.TextField(default='', null=True, verbose_name='Poster')),
                ('score', models.FloatField(default=0, verbose_name='Derived Actor Score')),
                ('imdb_mean', models.FloatField(default=0, verbose_name='Average IMDb Score')),
                ('imdb_votes', models.IntegerField(default=1, verbose_name='Order')),
                ('imdb_comp', models.FloatField(default=0, verbose_name='Average IMDb Score')),
            ],
        ),
        migrations.CreateModel(
            name='ActorCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.CharField(max_length=50, verbose_name='Character')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('castid', models.IntegerField(default=0, verbose_name='CastID')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Actor')),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='Subject')),
                ('sender', models.CharField(max_length=100, verbose_name='Subject')),
                ('cc_myself', models.CharField(max_length=100, verbose_name='Subject')),
                ('recipients', models.CharField(max_length=100, verbose_name='Subject')),
                ('message', models.TextField(max_length=1000, verbose_name='Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crewid', models.IntegerField(null=True, unique=True, verbose_name='ActorID')),
                ('job', models.CharField(default='', max_length=1, verbose_name='Job')),
                ('name', models.CharField(max_length=50, verbose_name='Crew Name')),
                ('score', models.FloatField(default=0, verbose_name='Derived Score')),
                ('imdb_mean', models.FloatField(default=0, verbose_name='Average IMDb Score')),
                ('imdb_votes', models.IntegerField(default=1, verbose_name='Order')),
                ('imdb_comp', models.FloatField(default=0, verbose_name='Average IMDb Score')),
                ('profilepath', models.TextField(default='', null=True, verbose_name='Poster')),
            ],
        ),
        migrations.CreateModel(
            name='CrewCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.CharField(max_length=50, null=True, verbose_name='Character')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='order')),
                ('crew', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Crew')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(default='', max_length=25, verbose_name='Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=300, verbose_name='Movie Title')),
                ('imdb_id', models.CharField(default='', max_length=9, verbose_name='IMDB ID')),
                ('rating', models.CharField(default='', max_length=25, null=True, verbose_name='Rating')),
                ('imdb_rating', models.DecimalField(decimal_places=1, default=0, max_digits=3, null=True, verbose_name='IMDb Rating')),
                ('imdb_votes', models.IntegerField(default=0, null=True, verbose_name='IMDb Votes')),
                ('metacritic_rating', models.IntegerField(default=0, null=True, verbose_name='Metacritic Rating')),
                ('lastUpdated', models.DateField(default=django.utils.timezone.now, verbose_name='lastUpdated')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Date')),
                ('plot', models.TextField(default='', null=True, verbose_name='Plot')),
                ('tagline', models.TextField(default='', null=True, verbose_name='Tagline')),
                ('fullplot', models.TextField(default='', null=True, verbose_name='FullPlot')),
                ('poster', models.TextField(default='', null=True, verbose_name='Poster')),
                ('awards', models.TextField(default='', null=True, verbose_name='Awards')),
                ('youtubeid', models.TextField(default='', max_length=24, verbose_name='YouTube ID')),
                ('tmdbdata', models.BooleanField(default=False)),
                ('adult', models.BooleanField(default=False)),
                ('runtime', models.PositiveSmallIntegerField(null=True)),
                ('language', models.TextField(default='', max_length=2, verbose_name='YouTube ID')),
            ],
        ),
        migrations.CreateModel(
            name='MovieTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(default='', max_length=30, verbose_name='Tag')),
                ('type', models.CharField(default='t', max_length=1, verbose_name='Tag Type')),
                ('movie', models.ManyToManyField(to='movies.Movie')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200, verbose_name='Question Text')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(default='None given', max_length=200, verbose_name='Reason')),
                ('vote', models.IntegerField(default=0, verbose_name='Votes')),
                ('op_rating', models.SmallIntegerField(default=99, verbose_name='Rate Suggestion')),
                ('op_message', models.TextField(default='')),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('votefrom', models.ManyToManyField(related_name='votefrom', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=8, verbose_name='Data Type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMovieRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watched', models.BooleanField()),
                ('rating', models.PositiveSmallIntegerField(default=99)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='genre',
            name='movie',
            field=models.ManyToManyField(to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='crewcredit',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='crew',
            name='credit',
            field=models.ManyToManyField(through='movies.CrewCredit', to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='actorcredit',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='actor',
            name='credit',
            field=models.ManyToManyField(through='movies.ActorCredit', to='movies.Movie'),
        ),
    ]
