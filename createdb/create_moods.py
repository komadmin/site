#!/usr/bin/python
import sys, os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siteroot.settings")
print('Python %s on %s' % (sys.version, sys.platform))
print('Django %s' % django.get_version())

if (__name__ == "__main__") & (len(sys.argv) > 1):
    server = sys.argv[1]
    if server == 'home':
        djangopath = '/home/darren/websites/komend/siteroot'
    elif server == 'server':
        djangopath = '/home/django/siteroot'
else:
    djangopath = '/home/darren/websites/komend/siteroot'


sys.path.extend([djangopath])
if 'setup' in dir(django):
    django.setup()
reload(sys)
sys.setdefaultencoding('utf8')




from createdb.moods import categories

from movies.models import MovieTags, Movie
from matplotlib import pyplot
from numpy import array, log
#
# catflat = list()
# for k, v in categories.iteritems():
#     catflat = catflat + v

#
#
# for m in movies[0:1]:
#     movie = Movie.objects.get(imdb_id=m['imdb_id'])
#     tagset = movie.movietags_set.all().values('pk')
#     mlist = []
#     tag = tagset[0]
#     for tag in tagset:
#         q = Movie.objects.filter(movietags__pk=int(tag['pk'])).order_by('-imdb_votes')[0:10].values('imdb_id')
#         mlist = mlist + [id['imdb_id'] for id in q]
#     mlistu = list(set(mlist))
#     mc = dict()
#     mu = mlistu[0]
#     ind = 0
#     for mu in mlistu:
#         ind += 1
#         print "%d of %d" % (ind, len(mlistu))
#         mc[mu] = mlist.count(mu)



#

from numpy import array
from django.db import transaction

tags = MovieTags.objects.all()

N = len(tags)

def addtagcounts():
    ind = 0
    with transaction.atomic():
        for t in tags:
            ind += 1
            if t.n != t.movie.all().count():
                t.n = t.movie.all().count()
                t.save()
            print "%d of %d: %s %d" % (ind, N, t.tag, t.n)

# addtagcounts()

otags = MovieTags.objects.filter(type='t').order_by('-n')

#


## TEST SIMILAR MOVIES

m = Movie.objects.get(imdb_id="tt1403865")

def findsimilar(m):
    t = m.movietags_set.filter(type='t')
    mf = Movie.objects
    for tag in t:
        print "Filtering Tag: %s" % tag.tag
        mf = mf.filter(movietags__tag=tag)
    mf = mf.order_by('-imdb_votes')
    return mf

m.movietags_set.all()

