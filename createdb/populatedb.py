
from movies.models import Movie, Actor, Question, Suggestion
from decimal import Decimal
import json
import tmdbsimple as tmdb
from datetime import date

tmdb.API_KEY = 'd7d0d2bfc8b2379fedded9dbd1f356b5'

fname = "/home/darren/websites/komend/data/tmdbJSON2.txt"

def get_data(imdbid="tt0816692"):
    t = tmdb.Movies(imdbid)
    movie = dict()
    movie["credits"] = t.credits()
    movie["info"] = t.info()
    movie["credits"] = t.credits()
    movie["keywords"] = t.credits()
    movie["videos"] = t.videos()
    return movie


movies = Movie.objects.all().order_by("-imdb_votes")

with open(fname, 'w') as f:
    for m in movies:
        j = json.dumps(get_data(imdbid=m.imdb_id))
        f.writelines(j + "\r\n")
        print "written %s" % m.title


f = open(fname,'r')
