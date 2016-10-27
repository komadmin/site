from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
## Create your models here.
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class Movie(models.Model):
    def __str__(self):
        return "%s" % self.title

    title = models.CharField('Movie Title', max_length=300, default='')
    imdb_id = models.CharField('IMDB ID', max_length=9, default='')
    rating = models.CharField('Rating', max_length=25, default='', null=True)
    runtime = models.CharField('Runtime', max_length=10, default='', null=True)
    imdb_rating = models.DecimalField('IMDb Rating', max_digits=3, decimal_places=1, default=0, null=True)
    imdb_votes = models.IntegerField('IMDb Votes',  default=0, null=True)
    metacritic_rating = models.IntegerField('Metacritic Rating', default=0, null=True)
    lastUpdated = models.DateField('lastUpdated', default=timezone.now)
    date = models.DateField('Date', default=timezone.now)
    plot = models.TextField('Plot', default='', null=True)
    tagline = models.TextField('Tagline', default='', null=True)
    fullplot = models.TextField('FullPlot', default='', null=True)
    poster = models.TextField('Poster', default='', null=True)
    postersaved = models.BooleanField(default=False)
    awards = models.TextField('Awards', default='', null=True)
    youtubeid = models.TextField('YouTube ID', max_length=24, default='')
    tmdbdata = models.BooleanField(default=False)
    adult = models.BooleanField(default=False)
    runtime = models.PositiveSmallIntegerField(null=True)
    language = models.TextField('YouTube ID', max_length=2, default='')
    similar = models.ManyToManyField('self', through='SimilarMovieRel', symmetrical=False)

    def actors(self, N=False):
        actorset = Crew.objects.filter(credit=self.pk, job='a').order_by('crewcredit__order')
        if not N:
            N = actorset.count()
        actorset = list(actorset[0:N])
        for ii in range(0, N):
            actorset[ii].character = actorset[ii].crewcredit_set.filter(movie=self.pk).first().character
        return actorset

    def tags(self,type='t'):
        m = Movie.objects.get(pk=self.pk)
        if type == 'all':
            return m.movietags_set.all()
        else:
            return m.movietags_set.filter(type=type)

    def actor_preview(self):
        return self.crewcredit_set.filter(crew__job="a").order_by('order')[0:2]

    def director_preview(self):
        return self.crewcredit_set.filter(crew__job="d").order_by('order')

        # for a in res:
        #     name.append(a.crew.name)
        #
        # return ', '.join(name)


class Genre(models.Model):
    def __str__(self):
        return "%s" % self.genre
    movie = models.ManyToManyField(Movie)
    genre = models.CharField('Genre', max_length=25, default='')


class SimilarMovieRel(models.Model):
    def __str__(self):
        return "%s to %s" % (self.linkfrom.title, self.linkto.title)
    linkfrom = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='linkfrom', null=True)
    linkto = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='linkto', null=True)
    basedon = models.CharField('Based On', max_length=5, default='')
    score = models.FloatField('Score')
    votes = models.IntegerField('Votes', default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    reason = models.CharField('Reason', max_length=200, default='None given')
    votefrom = models.ManyToManyField(User, related_name="simvotefrom")
    op_rating = models.SmallIntegerField('Rate Similar', default=99)
    op_message = models.TextField(default='')


class Actor(models.Model):
    def __str__(self):
        return "%s" % self.name
    id = models.IntegerField('ActorID', primary_key=True)
    name = models.CharField('Actor Name', max_length=50)
    profilepath = models.TextField('Poster', default='', null=True)
    score = models.FloatField('Derived Actor Score', default=0)
    imdb_mean = models.FloatField('Average IMDb Score', default=0)
    imdb_votes = models.IntegerField('Order', default=1)
    imdb_comp = models.FloatField('Average IMDb Score', default=0)
    credit = models.ManyToManyField(Movie, through='ActorCredit')


class ActorCredit(models.Model):
    def __str__(self):
        return "%s" % self.character
    character = models.CharField('Character', max_length=50)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    order = models.IntegerField('Order', default=0)
    castid = models.IntegerField('CastID', default=0)


class Crew(models.Model):
    def __str__(self):
        return "%s as %s" % (self.name, self.character)
    crewid = models.IntegerField('ActorID', unique=True, null=True)
    credit = models.ManyToManyField(Movie, through='CrewCredit')
    job = models.CharField('Job', max_length=1, default='')
    name = models.CharField('Crew Name', max_length=50)
    score = models.FloatField('Derived Score', default=0)
    imdb_mean = models.FloatField('Average IMDb Score', default=0)
    imdb_votes = models.IntegerField('Order', default=1)
    imdb_comp = models.FloatField('Average IMDb Score', default=0)
    profilepath = models.TextField('Poster', default='', null=True)
    character = 'removeme'


class CrewCredit(models.Model):
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
    character = models.CharField('Character', max_length=50, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField('order', default=0)


class Question(models.Model):
    def __str__(self):
        return "%s" % self.question_text

    question_text = models.CharField('Question Text', max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Suggestion(models.Model):
    def __str__(self):
        return "Suggestion"

    user = models.ForeignKey(User, on_delete=models.CASCADE) # same answer can't apply to different users
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # same answer can't apply to different questions
    answer = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True) # suggestion can apply to many questions and vice versa
    reason = models.CharField('Reason', max_length=200, default='None given')
    vote = models.IntegerField('Votes', default=0)
    votefrom = models.ManyToManyField(User, related_name="votefrom")
    op_rating = models.SmallIntegerField('Rate Suggestion', default=99)
    op_message = models.TextField(default='')


class MovieTags(models.Model):
    def __str__(self):
        return "%s" % self.tag

    movie = models.ManyToManyField(Movie)
    tag = models.CharField('Tag', max_length=30, default='')
    type = models.CharField('Tag Type', max_length=1, default='t')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    n = models.IntegerField('Count', default=0)
    # id = models.IntegerField('ID')


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField('Data Type', max_length=8, default='')
    # data = JSONField()


class UserMovieRating(models.Model):
    def __str__(self):
        return "Pref: %s" % self.user

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched = models.BooleanField()
    rating = models.PositiveSmallIntegerField(default=99)


class ContactUs(models.Model):
    def __str__(self):
        return "Contacts"

    subject = models.CharField('Subject', max_length=100)
    sender = models.CharField('Subject', max_length=100)
    cc_myself = models.CharField('Subject', max_length=100)
    recipients = models.CharField('Subject', max_length=100)
    message = models.TextField('Subject', max_length=1000)
