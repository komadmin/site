#!/usr/bin/python
import sys, os, time, json, pprint, django, glob, codecs
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siteroot.settings")
print('Python %s on %s' % (sys.version, sys.platform))
print('Django %s' % django.get_version())


if (__name__ == "__main__") & (len(sys.argv) > 1):
    server = sys.argv[1]
    if server == 'home':
        fname = "/home/darren/websites/komend/db/tmdb*.txt"
        djangopath = '/home/darren/websites/komend/siteroot'
    elif server == 'server':
        fname = "/home/django/db/tmdb*.txt"
        djangopath = '/home/django/siteroot'
else:
    fname = "/home/darren/websites/komend/db/tmdb*.txt"
    djangopath = '/home/darren/websites/komend/siteroot'

sys.path.extend([djangopath])
if 'setup' in dir(django):
    django.setup()
reload(sys)
sys.setdefaultencoding('utf8')



def readalllines(fnamepattern, limit):
    ind = 0
    flist = sorted(glob.glob(fnamepattern))
    for fname in flist:
        with codecs.open(fname, 'r', 'ISO-8859-1') as f:
            for line in f:
                try:
                    line = line.replace('\r\n','')
                    d = json.loads(line)
                    yield d
                    ind += 1
                    if ind >= limit:
                        return
                except:
                    yield None



def findorcreate(Obj, tag):
    o = Obj.objects.filter(tag=tag)
    if not o:
        print "Creating %s" % tag
        o = Obj(tag=tag, type='k')
        o.save()
    else:
        o = o[0]
    return o


from movies.models import *

for d in readalllines(fnamepattern=fname, limit=1e10):
    try:
        keywords = d['keywords']['keywords']
        m = Movie.objects.filter(imdb_id=d['imdbid']).first()
        if m:
            for k in keywords:
                try:
                    tag = findorcreate(MovieTags, k['name'])
                    if not m.movietags_set.filter(tag=k['name']):
                        tag.movie.add(m)
                        print "Adding %s to %s" % (k['name'], d['imdbid'])
                    else:
                        print "Already added: %s to %s" % (k['name'], d['imdbid'])
                except:
                    print "Failed to add %s" % k['name']
    except:
        pass
