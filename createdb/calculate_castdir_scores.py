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


from movies.models import Crew

allact = Crew.objects.filter(job="a").values('pk')
allwri = Crew.objects.filter(job="w").values('pk')
alldir = Crew.objects.filter(job="d").values('pk')

Nact = allact.count()
Ndir = alldir.count()
Nwri = allwri.count()
Ntot = Nact + Ndir + Nwri

#

def findmax(l):
    max_val = max(l)
    max_idx = l.index(max_val)
    return max_idx, max_val

ind = 0

for ty in [allact, allwri, alldir]:
    for A in ty:
        try:
            ind += 1
            a = Crew.objects.get(pk=A['pk'])
            mlist = a.credit.values('imdb_rating', 'imdb_votes')
            scores = [float(m['imdb_rating']) for m in mlist]
            Nvotes = sum([int(m['imdb_votes']) for m in mlist])
            a.imdb_votes = Nvotes
            a.imdb_mean = sum(scores)/len(scores)
            a.imdb_comp = Nvotes * sum(scores)/len(scores)
            perc = float(ind) / float(Ntot) * 100
            a.save()
            print "%2.5f, imdb score = %2.1f, %s : %s" % (perc,  a.imdb_mean, a.name, a.job)
        except:
            print "failed"
