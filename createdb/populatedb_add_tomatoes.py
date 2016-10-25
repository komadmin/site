#!/usr/bin/python
import sys, os, django, codecs, re
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siteroot.settings")
print('Python %s on %s' % (sys.version, sys.platform))
print('Django %s' % django.get_version())

if (__name__ == "__main__") & (len(sys.argv) > 1):
    server = sys.argv[1]
    if server == 'home':
        fname = "/home/darren/websites/komend/data/tomatoes.txt"
        djangopath = '/home/darren/websites/komend/siteroot'
    elif server == 'server':
        fname = "/home/django/db/tomatoes.txt"
        djangopath = '/home/django/siteroot'
else:
    fname = "/home/darren/websites/komend/data/tomatoes.txt"
    djangopath = '/home/darren/websites/komend/siteroot'


sys.path.extend([djangopath])
if 'setup' in dir(django):
    django.setup()
reload(sys)
sys.setdefaultencoding('utf8')


from movies.models import Movie


def int2(stringval):
    if not stringval:
        i = 0
    else:
        i = int(stringval)
    return i

def dec2(stringval):
    if not stringval:
        return float(0)
    else:
        return float(stringval)


import subprocess
L = subprocess.check_output(['wc', '-l', fname])
L = int(L.replace(fname,'').replace('\n','').strip())
print L


# Check data is okay
tom = list()
with codecs.open(fname, 'r', 'ISO-8859-1') as f:
    l = f.readline().replace('\r\n', '')
    names = l.split('\t')
    for line in f:
        l = line.replace('\r\n', '').split('\t')
        d = {names[ii]: l[ii] for ii in range(0, len(l))}
        # tom.append(d)
        if Movie.objects.get(imdb_id='%0.7d' % d['ID']):
            m = Movie.objects.get(imdb_id='%0.7d' % d['ID'])


