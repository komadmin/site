#!/usr/bin/python
import sys, os, time, json, pprint, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siteroot.settings")
print('Python %s on %s' % (sys.version, sys.platform))
print('Django %s' % django.get_version())
sys.path.extend(['/home/django/siteroot'])
if 'setup' in dir(django):
    django.setup()

from movies.models import Movie
import tmdbsimple as tmdb

def printdict(d):
    print(json.dumps(d, sort_keys=False, indent=2))

tmdb.API_KEY = 'd7d0d2bfc8b2379fedded9dbd1f356b5'

# fname = "/home/django/tmdbJSON2.txt"
fname = "/home/darren/websites/komend/db/tmdbJSON2.txt"


def get_data(imdbid="tt0816692"):
    t = tmdb.Movies(imdbid)
    movie = dict()
    funs = {"credits": t.credits, "info": t.info, "keywords":t.keywords, "videos":t.videos}
    for key in funs:
        try:
            movie[key] = funs[key]()
        except:
            print "Could not load %s" % key

    movie["imdbid"] = imdbid
    return movie


idlist = list()
with open(fname,'r') as f:
    for line in f:
        l = json.loads(line.replace('\r\n',''))
        idlist.append(l["imdbid"])
        print idlist


movies = Movie.objects.all().order_by("-imdb_votes")[0:10000]


with open(fname, 'a') as f:
    # for ii in range(0,len(movies)):
    # m = movies[ii]
    for m in movies:
        if m.imdb_id not in idlist:
            try:
                print "getting data"
                j = json.dumps(get_data(imdbid=m.imdb_id))
                f.writelines(j + "\r\n")
                print "written %s" % m.title
                time.sleep(1)
            except:
                print "failed %s " % m.title
                time.sleep(1)



