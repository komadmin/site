import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siteroot.settings")
print('Python %s on %s' % (sys.version, sys.platform))
import django
print('Django %s' % django.get_version())
sys.path.extend(['/home/darren/websites/komend/siteroot'])
if 'setup' in dir(django):
    django.setup()


from movies.models import Movie, Actor, Crew
import codecs

fname = "/home/darren/websites/komend/data/omdbMovies.txt"

li = 0
with open(fname) as f:
    for line in f:
        li += 1

f = codecs.open(fname, 'r', 'ISO-8859-1')
l = f.readline().replace('\r\n', '')
names = l.split('\t')

# Actor.objects.all().delete()
# Director.objects.all().delete()

def add_cast(cast, m, Obj, setname):
    if len(cast[0]) == 0:
        return

    ind = 0
    for c in cast:
        ind += 1
        c = c.strip()
        if len(c) > 50: c = c[0:50]
        a = Obj.objects.filter(name=c)
        if len(a) == 0:
            a = Obj(name=c, order=ind)
            a.save()
            a.movie.add(m)
            a.save()
        else:
            a = a[0]
            if hasattr(m, setname):
                v = getattr(m, setname).filter(pk=a.pk)
                if len(v) == 0:
                    a.movie.add(m)
                    a.save()
                    print "Saving %s: %s in Movie: %s" % (setname, c, m.title)
                else:
                    print "Actor %s already added to %s" % (a.name, m.title)
            else:
                a.movie.add(m)
                a.save()
                print "Saving %s: %s in Movie: %s" % (setname, c, m.title)



imdb = {m.imdb_id:m.pk for m in Movie.objects.all()} # much faster than trying to loop through imdbID lookups in database


for ii in range(0, li):
    l = f.readline().replace('\r\n', '').split('\t')
    if (ii >= 0) and (len(l) == len(names)):
        d = {names[ii]: l[ii] for ii in range(0, len(l))}
        if d["imdbID"] in imdb:
            ml = Movie.objects.filter(pk=imdb[d["imdbID"]])
            print d["imdbID"]
            if ml.exists():
                ml = ml[0]
                if hasattr(ml,"actor_set"): # actor_set needs to exist first
                    cast = d["Cast"].split(',')
                    if len(ml.actor_set.all()) != len(cast):
                        add_cast(cast, ml, Actor, 'actor_set')
                    else:
                        print(d["imdbID"] + " Actor Length Matches")
                elif len(cast) != 0:
                    add_cast(cast, ml, Actor, 'actor_set')

                if hasattr(ml, "director_set"):
                    director = d["Director"].split(',')
                    if len(ml.director_set.all()) != len(director):
                        add_cast(director, ml, Director, 'director_set')
                    else:
                        print(d["imdbID"] + " Director Length Matches")
                elif len(cast) != 0:
                    add_cast(director, ml, Actor, 'director_set')

            else:
                print(d["imdbID"] + "Not found")
