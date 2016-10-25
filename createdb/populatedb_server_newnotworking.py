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

print "loading m"
movies = Movie.objects.all().order_by("-imdb_votes")
L = movies.count()

pklist = list()
S = 30000
step = 10000
# L = 30300 # debugging
for ii in range(S, L, step):
    movies = Movie.objects.all().order_by("-imdb_votes")[ii-step:ii]
    pk = [m.pk for m in movies]
    pklist = pklist + pk # concat is a plus sign
    print str(ii)


print str(len(pklist))

fnameind = 1
fname = "/home/django/tmdbJSON%0.3d.txt" % fnameind
print fname
# fname = "/home/darren/websites/komend/db/tmdbJSON1.txt"

def read_open_file(fname):
    if os.path.isfile(fname):
        print "file exists"
        with open(fname,'r') as f:
            print "reading file"
            for line in f:
                l = json.loads(line.replace('\r\n',''))
                idlist.append(l["imdbid"])    
        f.close()
        f = open(fname, 'a')
    else:
        print "file does not exist: opening file for writing"
        f = open(fname, 'w')
    return f

f = read_open_file(fname)

ind = 0
print "going through list"
print "%d" % L


for ii in range(0, len(pklist)):
    print str(ii)
    ind += 1
    try:
        m = Movie.objects.get(pk=pklist[ii])
        imdbid = m.imdb_id
        title = m.title
        # if ind > 10000 switch files an continue
        if ind > 1000:
            fnameind += 1
            ind = 0
            fname = "/home/django/tmdbJSON%0.3d.txt" % fnameind
            f = read_open_file(fname)

        if imdbid not in idlist:
            try:
                print "getting data"
                j = json.dumps(get_data(imdbid=imdbid))
                f.writelines(j + "\r\n")
                print "written %s" % title
                time.sleep(1)
            except:
                print "failed %s" % title
                time.sleep(1)
        else:
            print "%s already in list" % title
    except:
        print "Error"
  