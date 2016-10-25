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



##

from movies.models import *
from django.db import transaction

M = Movie.objects.order_by('-imdb_votes')

SimilarMovieRel.objects.all().delete()

def create_similar_links(m):
    t = m.movietags_set.filter(type='t').order_by('-n')
    mf = Movie.objects
    for tag in t:
        mf = mf.filter(movietags__tag=tag)

    mf = mf.order_by('-imdb_votes')[0:50]
    print m.movietags_set.filter(type='t').order_by('-n')
    for r in mf:
        if SimilarMovieRel.objects.filter(linkfrom=m, linkto=r, basedon='tmain', score=0):
            continue
        if r.imdb_id == m.imdb_id:
            continue
        s = SimilarMovieRel(linkfrom=m, linkto=r, basedon='tmain', score=0)
        s.save()
    return None

# with transaction.atomic():
for ii in range(1, 10):
    m = M[ii]
    create_similar_links(m)
    print m.similar.all()
