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


sys.path.extend([djangopath])
if 'setup' in dir(django):
    django.setup()
reload(sys)
sys.setdefaultencoding('utf8')

from movies.models import Movie, Crew, CrewCredit
from datetime import date


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


f = codecs.open(fname, 'r', 'ISO-8859-1')
l = f.readline().replace('\r\n', '')
names = l.split('\t')


addcrew = ['Director', 'Writer']
crewlabels = dict(Director='d', Writer='w')
updateimdbscores = True


ci2 = 0
for line in f:
    ci2 += 1
    # c = ci2/ci
    # line = f.readline()
    l = line.replace('\r\n', '').split('\t')
    d = {names[ii]: l[ii] for ii in range(0, len(l))}
    # print d['Released']
    # m = Movie.objects.filter(imdb_id__exact=d['imdbID'])
    saved = False
    if len(d) == 21:
        try:
            if d['imdbRating'] == '':
                continue
            mv = d
            if not (len(mv['Released']) > 7 & len(mv['imdbRating']) == 3): # & len(mv['Writer']) > 0:
                continue

            if len(mv['Metacritic']) == 0:
                mv['Metacritic'] = u'0'
            m = Movie.objects.filter(imdb_id=mv["imdbID"])

            if not m:
                # create new
                m = Movie(
                    title=mv["Title"],
                    imdb_id=mv["imdbID"],
                    rating=mv["Rating"],
                    date=date(int2(mv["Released"][0:4]), int2(mv["Released"][5:7]), int2(mv["Released"][8:10])),
                    imdb_rating = dec2(mv['imdbRating']),
                    imdb_votes = int2(mv['imdbVotes']),
                    metacritic_rating = int2(mv['Metacritic']),
                    lastUpdated = date(int2(mv["lastUpdated"][0:4]), int2(mv["lastUpdated"][5:7]), int2(mv["lastUpdated"][8:10])),
                    plot = mv['Plot'],
                    fullplot = mv['FullPlot'],
                    poster = mv['Poster'],
                    awards = mv['Awards'],
                    tmdbdata = False
                )
                m.save()
                saved = True
                print "Creating %s" % (m.title)

                # Only add crew and actors if movie didn't already exist.
                for crewtype in addcrew:
                    crew = mv[crewtype].split(',')
                    if crew:
                        for w in crew:
                            if w:
                                w = w.strip()
                                if len(w) > 50:
                                    w = re.sub('(\(\w+\))', '', w).strip()
                                    w = w[0:50]
                                cr = Crew.objects.filter(name=w, job=crewlabels[crewtype])
                                if not cr:
                                    cr = Crew(name=w, job=crewlabels[crewtype])
                                    cr.save()
                                    saved = True
                                    print "Creating %s %s" % (crewtype, w)
                                else:
                                    cr = cr[0]
                                    crc = CrewCredit.objects.filter(movie=m).filter(crew=cr)
                                    if not crc:
                                        crc = CrewCredit(movie=m, crew=cr)
                                        crc.save()
                                        saved = True
                                        print "Adding %s %s to %s" % (crewtype, w, m.title)

                        actors = mv['Cast'].split(',')
                        actors = [a.strip() for a in actors]
                        for actor in actors:
                            if actor:
                                w = actor
                                if len(w) > 50:
                                    w = re.sub('(\(\w+\))', '', w).strip()
                                    w = w[0:50]
                                a = Crew.objects.filter(name=actor, job='a').first()
                                if not a:
                                    a = Crew(name=actor, job='a')
                                    a.save()
                                    saved = True
                                else:
                                    crc = CrewCredit(movie=m, crew=a)
                                    crc.save()
                                    saved = True
                                    print "Adding %s %s to %s" % (crewtype, w, m.title)

                    else:
                        m = m[0]
                        sv = False
                        if (not m.plot) & (mv['Plot'] != u''):
                            m.plot = mv['Plot']
                            sv = True
                            print "Adding plot to %s" % (m.title)
                        if (not m.rating) & (mv['Rating'] != u''):
                            m.plot = mv['Rating']
                            sv = True
                            print "Adding rating to %s" % (m.title)
                        if (not m.metacritic_rating == int(mv['Metacritic'])):
                            m.metacritic_rating = mv['Metacritic']
                            sv = True
                            print "Adding metacritic to %s" % (m.title != '')
                        if (not m.poster) & (mv['Poster'] != ''):
                            m.poster = mv['Poster']
                            sv = True
                            print "Adding poster to %s (%s)" % (m.title, mv['Poster'])
                        if m.date.year != int(mv["Released"][0:4]):
                            m.date = date(int(mv["Released"][0:4]), int(mv["Released"][5:7]), int(mv["Released"][8:10]))
                            sv = True
                            print "Adding date to %s" % (m.title)
                        if float(m.imdb_rating) != dec2(mv['imdbRating']):
                            m.imdb_votes = int2(mv['imdbVotes'])
                            m.imdb_rating = dec2(mv['imdbRating'])
                            sv = True
                            print "Adding imdb ratings to %s" % (m.title)
                        # else:
                            # print "Rating okay for %s" % (m.title)
                        if sv:
                            m.save()
                            saved = True
        except:
            pass
        if not saved:
            print "Skipped: %s" % mv['imdbID']