from movies.models import Movie, Actor, Question, Suggestion
import json
from datetime import date

import csv

fname = "/home/darren/websites/komend/data/omdbMovies.txt"

def add_movie(mv):
    if len(mv['Released']) > 7 & len(mv['imdbRating']) == 3:
        if len(mv['Metacritic']) == 0:
            mv['Metacritic'] = u'0'

        m = Movie(
            title=mv["Title"],
            imdb_id=mv["imdbID"],
            rating=mv["Rating"],
            date=date(int(mv["Released"][0:4]), int(mv["Released"][5:7]), int(mv["Released"][8:10])),
            runtime = mv['Runtime'],
            genre = mv['Genre'],
            imdb_rating = float(mv['imdbRating']),
            imdb_votes = int(mv['imdbVotes']),
            metacritic_rating = int(mv['Metacritic']),
            lastUpdated = date(int(mv["lastUpdated"][0:4]), int(mv["lastUpdated"][5:7]), int(mv["lastUpdated"][8:10])),
            plot = mv['Plot'],
            fullplot = mv['FullPlot'],
            poster = mv['Poster'],
            awards = mv['Awards']
        )
        m.save()
        print("%s %s" % (ci2, mv["Title"]))


import codecs
f = codecs.open(fname, 'r', 'ISO-8859-1')
l = f.readline().replace('\r\n', '')
names = l.split('\t')

#
ci2 = 0
for line in f:
    ci2 += 1
    # c = ci2/ci
    l = line.replace('\r\n', '').split('\t')
    d = {names[ii]: l[ii] for ii in range(0, len(l))}
    # m = Movie.objects.filter(imdb_id__exact=d['imdbID'])
    if len(d) == 21:
        try:
            if d['imdbRating'] != '':
                add_movie(d)
            print('%s ' % ci2 + d['Title'] + '   ' + d['Rating'])

        except:
            print('%s %s %s %s' % (ci2, 'Error  ', d['Title'], d['imdbRating']))


##
from django.contrib.auth.models import User
from movies.models import Movie, Actor, Question, Suggestion
# user = User.objects.create_user('testuser3', 'dprice80@gmail.com', 'password')
# user.save()
#
# user = User.objects.create_user('testuser4', 'dprice80@gmail.com', 'password')
# user.save()

print len(Movie.objects.all())
print len(Actor.objects.all())

# Set some user preferences

u = User.objects.get(username='testuser3')
u2 = User.objects.get(username='testuser4')

Question.objects.all().delete()
Question(question_text="What's a Good Movie?", user=u).save()
Question(question_text="What's a Bad Movie?", user=u).save()
Question(question_text="What's a Terrible Movie?", user=u).save()
Question(question_text="What's a Funny Movie?", user=u).save()
Question(question_text="What's a Scary Movie?", user=u).save()
Question(question_text="What's a Weird Movie?", user=u).save()
Question(question_text="What's a Short Movie?", user=u).save()

