#!/usr/bin/python
import sys, os, json, django, glob, time, re

#if __name__ == "__main__":
#    print "using command line settings"
#    fname = sys.argv[1]
#    djangopath = sys.argv[2]
#    if sys.argv[3] == '--wipedb':
#        wipedb = True
#    else:
#        wipedb = False
#else:
print "not using command line"
fname = "/home/django/db/tmdb*txt"
djangopath = '/home/django/siteroot'
wipedb = True

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siteroot.settings")
print('Python %s on %s' % (sys.version, sys.platform))
print('Django %s' % django.get_version())
sys.path.extend([djangopath])
if 'setup' in dir(django):
    django.setup()

reload(sys)
sys.setdefaultencoding('utf8')

from movies.models import Movie, Actor, Crew, CrewCredit, Genre, ActorCredit, Question, Suggestion
from django.utils import timezone

if wipedb:
    print "wiping database"
    Actor.objects.all().delete()
    Movie.objects.all().delete()
    Crew.objects.all().delete()
    Question.objects.all().delete()
    Suggestion.objects.all().delete()


def printdict(d):
    print(json.dumps(d, sort_keys=False, indent=2))


# def add_movies_from_tmdb_file(fname):
flist = sorted(glob.glob(fname))
totind = 0

addcrew = ['Director', 'Writer', 'Producer']
crewlabels = dict(Director='d', Writer='w', Producer='p')

for fname in flist:
    #
    ind = 0
    with open(fname, 'r') as f:
        for line in f:
            ind += 1

    f = open(fname, 'r')
    for ii in range(0, ind):
        line = f.readline()
        totind += 1
        print totind
        if ii >= 0:
            try:
                j = json.loads(line)
                if 'info' in j:
                    print j['info']['title']
                    mov = j['info']
                    # Create Genre or add movie to genre

                    if not Movie.objects.filter(imdb_id=j['imdbid']):
                        m = Movie(
                            imdb_id=j['imdbid'],
                            title=mov['title'],
                            rating='',
                            runtime=mov['runtime'],
                            imdb_rating=mov['vote_average'],
                            imdb_votes=mov['vote_count'],
                            fullplot=mov['overview'],
                            plot='',
                            tagline=mov['tagline'],
                            poster='',
                            date=timezone.now(),
                            awards='',
                            youtubeid='',
                            tmdbdata=True,
                            adult=mov['adult']
                        )
                        m.save()
                    else:
                        print "Not creating %s" % j['info']['title']
                        m = Movie.objects.get(imdb_id=j['imdbid'])

                    for genre in mov['genres']:
                        if not Genre.objects.filter(genre=genre['name']):
                            g = Genre(genre=genre['name'])
                            g.save()
                        g = Genre.objects.get(genre=genre['name'])
                        g.movie.add(m)
                        g.save()
                    for actor in j['credits']['cast']:
                        if not Crew.objects.filter(crewid=actor['id']):
                            print "Creating actor: %s:: %s as %s" % (j['info']['title'], actor['name'], actor['character'])
                            a = Crew(crewid=actor['id'], name=actor['name'], profilepath=actor['profile_path'], job='a')
                            a.save()
                        else:
                            a = Crew.objects.get(crewid=actor['id'])

                        if not CrewCredit.objects.filter(movie=m).filter(crew=a):
                            if len(actor['character']) > 50:
                                actor['character'] = actor['character'][0:50]
                            print "Adding %s to Movie: %s" % (actor['name'], m.title)
                            ac = CrewCredit(character=actor['character'], crew=a, movie=m, order=actor['order'])
                            ac.save()

                    for crew in j['credits']['crew']:
                        crew['name'] = re.sub('(\(\w+\))', '', crew['name']).strip()
                        if crew['job'] in addcrew:
                            if not Crew.objects.filter(name=crew['name']).filter(job=crewlabels[crew['job']]):
                                print "Creating Crew: %s" % crew['name']
                                cr = Crew(name=crew['name'], job=crewlabels[crew['job']])
                                cr.save()
                            else:
                                print "Already exists: %s" % crew['name']
                                cr = Crew.objects.get(name=crew['name'], job=crewlabels[crew['job']])

                            if not CrewCredit.objects.filter(movie=m).filter(crew=cr):
                                print "Adding %s to Movie: %s" % (crew['name'], m.title)
                                cc = CrewCredit(crew=cr, movie=m)
                                cc.save()
            except: 
                print "Error %s" % j['imdbid']
                m = Movie(title="Unknown Error", imdb_id=j['imdbid'])
                m.save()


    f.close()


#
# ## Get a list of missing IDs
# missinglist = []
# for fname in flist:
#     #
#     ind = 0
#     with open(fname, 'r') as f:
#         for line in f:
#             j = json.loads(line)
#             if not Movie.objects.filter(imdb_id=j['imdbid']):
#                 print "%s Doesn't exist" % j['imdbid']
#                 missinglist.append(j['imdbid'])
#             else:
#                 print "%s Exists" % j['imdbid']
#
#     # add_movies_from_tmdb_file(fname)
#
#
### Check only those IDs that do not exist in database
#
# import tmdbsimple as tmdb
# tmdb.API_KEY = 'd7d0d2bfc8b2379fedded9dbd1f356b5'
# t = tmdb.Movies(missinglist[10])
# funs = {"credits": t.credits(), "info": t.info(), "keywords": t.keywords(), "videos": t.videos()}
#
# for fname in flist:
#     #
#     ind = 0
#     with open(fname, 'r') as f:
#         for line in f:
#             ind += 1
#
#     f = open(fname, 'r')
#     for ii in range(0, ind):
#         line = f.readline()
#         j = json.loads(line)
#         if j['imdbid'] in missinglist:
#         # try:
#             if 'info' in j:
#                 print j['info']['title']
#                 mov = j['info']
#                 # Create Genre or add movie to genre
#
#                 if not Movie.objects.filter(imdb_id=j['imdbid']):
#                     m = Movie(
#                         imdb_id=j['imdbid'],
#                         title=mov['title'],
#                         rating='',
#                         runtime=mov['runtime'],
#                         imdb_rating=mov['vote_average'],
#                         imdb_votes=mov['vote_count'],
#                         fullplot=mov['overview'],
#                         plot='',
#                         tagline=mov['tagline'],
#                         poster='',
#                         date=timezone.now(),
#                         awards='',
#                         youtubeid='',
#                         tmdbdata=True,
#                         adult=mov['adult']
#                     )
#                     m.save()
#                 else:
#                     print "Not creating %s" % j['info']['title']
#                     m = Movie.objects.get(imdb_id=j['imdbid'])
#
#                 for genre in mov['genres']:
#                     if not Genre.objects.filter(genre=genre['name']):
#                         g = Genre(genre=genre['name'])
#                         g.save()
#                     g = Genre.objects.get(genre=genre['name'])
#                     g.movie.add(m)
#                     g.save()
#                 for actor in j['credits']['cast']:
#                     if not Actor.objects.filter(id=actor['id']):
#                         print "Creating actor: %s:: %s as %s" % (j['info']['title'], actor['name'], actor['character'])
#                         if len(actor['character']) > 50:
#                             actor['character'] = actor['character'][0:50]
#                         a = Actor(id=actor['id'], name=actor['name'], profilepath=actor['profile_path'])
#                         a.save()
#                     else:
#                         a = Actor.objects.get(id=actor['id'])
#
#                 for crew in j['credits']['crew']:
#                     addcrew = ['Director', 'Writer']
#                     if crew['job'] in addcrew:
#                         if not Crew.objects.filter(name=crew['name']):
#                             print "Creating Crew: %s" % crew['name']
#                             cr = Crew(name=crew['name'])
#                             cr.save()
#                         else:
#                             print "Already exists: %s" % crew['name']
#                             cr = Crew.objects.get(name=crew['name'])
#
#                     if not CrewCredit.objects.filter(movie=m).filter(crew=cr):
#                         print "Adding %s to Movie: %s" % (crew['name'], m.title)
#                         cc = CrewCredit(crew=cr, movie=m, job=crew['job'], order=0)
#                         cc.save()
#         # except:
#         #     print "Error %s" % j['imdbid']
#         #     m = Movie(title="Unknown Error", imdb_id=j['imdbid'])
#         #     m.save()
#         #     time.sleep(5)
#
#     f.close()
