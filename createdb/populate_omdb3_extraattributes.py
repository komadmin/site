#!/usr/bin/python
import sys, os, django, codecs, re
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siteroot.settings")
print('Python %s on %s' % (sys.version, sys.platform))
print('Django %s' % django.get_version())

if (__name__ == "__main__") & (len(sys.argv) > 1):
    server = sys.argv[1]
    if server == 'home':
        fname = "/home/darren/websites/komend/data/omdbMovies.txt"
        djangopath = '/home/darren/websites/komend/siteroot'
    elif server == 'server':
        fname = "/home/django/db/omdbMovies.txt"
        djangopath = '/home/django/siteroot'
else:
    fname = "/home/darren/websites/komend/data/omdbMovies.txt"
    djangopath = '/home/darren/websites/komend/siteroot'

sys.path.extend([djangopath])
if 'setup' in dir(django):
    django.setup()
reload(sys)
sys.setdefaultencoding('utf8')

from movies.models import MovieTags, Movie


f = codecs.open(fname, 'r', 'ISO-8859-1')
l = f.readline().replace('\r\n', '')
names = l.split('\t')

from django.db import transaction

for line in f:
    try:
        with transaction.atomic():
            l = line.replace('\r\n', '').split('\t')
            d = {names[ii]: l[ii] for ii in range(0, len(l))}
            tags = d['Genre'].split(",")
            tags = [tag.strip() for tag in tags]
            print d['imdbID']
            m = Movie.objects.filter(imdb_id=d['imdbID'])
            if m:
                m = m[0]
                for tag in tags:
                    t = MovieTags.objects.filter(tag=tag)
                    if t:
                        t = t[0]
                    elif tag:
                        t = MovieTags(tag=tag)
                        t.save()
                        print "Created tag %s, and added %s" % (tag, m.title)
                    else:
                        print "Genre empty"
                    if t:
                        if not MovieTags.objects.filter(tag=tag, movie=m):
                            t.movie.add(m)
                            print "Added tag %s to %s" % (tag, m.title)
                        else:
                            print "Tag %s exists in %s" % (tag, m.title)
    except KeyboardInterrupt:
        raise(KeyboardInterrupt)
    except:
        print "failed"