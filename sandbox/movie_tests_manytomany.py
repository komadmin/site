from movies.models import MovieMany, ActorMany

MovieMany.objects.all().delete()
ActorMany.objects.all().delete()

m = MovieMany(title='Dumb and Dumber')
m2 = MovieMany(title='Dumb and Dumber2')
a = ActorMany(first_name="Jim",last_name="Carrey")
a2 = ActorMany(first_name="Jeff",last_name="Daniels")

# need to save before associating it with a publication

a.save()
a2.save()
m.save()
m2.save()

m.actor.add(a)

m2.actor.add(a,a2)

m2.save()
m.save()

# create and add in one step
newa = m.actor.create(first_name="Joe",last_name="Bloggs")
newa.save()
m.save()
m.actor.all()
# actor = publication, movie = article
newa.moviemany_set.all()

# can search using ids, or the object itself.
actorid = a.id
MovieMany.objects.filter(actor__pk=actorid)

MovieMany.objects.filter(actor=a)

MovieMany.objects.filter(actor__first_name__contains="Ji")

MovieMany.objects.filter(actor__in=[a,a2]).distinct()

# more examples at https://docs.djangoproject.com/en/1.10/topics/db/examples/many_to_many/

m3 = MovieMany(title="IT Crowd")
m3.save()
a.moviemany_set.add(m3)
a.save()

