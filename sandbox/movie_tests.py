from movies.models import Movie, Actor
from datetime import date

# create 2 actors
a = Actor(first_name="Darren", last_name="Price")
a.save()

a2 = Actor(first_name="Darren2", last_name="Price2")
a2.save()

# create movie
m = Movie(title="Dumb", release_date=date(2016,7,8), rating=10, actor=a)
m.save()

a = m.actor

# create movie object via the actor object relationship
new_movie = a.movie_set.create(title="Dumb set using _set", release_date=date(2016,7,8), rating=10)

# adding a movie to the movie set (a movie set is defined for an actor)
m2 = Movie(title="Dumb and Dumberer", release_date=date(2016,7,8), rating=10)
m2.save()

# adding movie to a different actor has the effect of moving the movie to a different set
# this is Many to One!! so the movie cannot belong to two actors at once. We need Many to Many
a.movie_set.add(m2)

a2.movie_set.add(m2)

Movie.objects.all()
Actor.objects.order_by('first_name')

Movie.objects.all().delete()

Movie.objects.all()
Actor.objects.all().delete()
Actor.objects.all()

reset(m)


