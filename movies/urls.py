from django.conf.urls import url

from . import views

app_name = 'movies' # naming the app for namespacing

urlpatterns = [
    url(r'^movielist/$', views.listmovies, name='movielist'),
    url(r'^similarmoviessimple/(?P<movie_id>[0-9]+)/$', views.similarmoviessimple, name='similarmoviessimple'),
    url(r'^similarmovies/(?P<movie_id>[0-9]+)/$', views.similarmovies, name='similarmovies'),
    url(r'^addsimilar_ajax/$', views.addsimilar_ajax, name='addsimilar_ajax'),
    url(r'^votesimilar/$', views.votesimilar, name="votesimilar"),
    url(r'^markasseen/$', views.markasseen, name="markasseen"),
    url(r'^moviedetail/(?P<movie_id>[0-9]+)/$', views.moviedetail, name='moviedetail'),
    url(r'^actorlist/$', views.listactors, name='actorlist'),
    url(r'^directorlist/$', views.listdirectors, name='directorlist'),
    url(r'^actordetail/(?P<actor_id>[0-9]+)/$', views.actordetail, name='actordetail'),
    url(r'^directordetail/(?P<director_id>[0-9]+)/$', views.directordetail, name='directordetail'),
    url(r'^questionlist/$', views.questionlist, name='questionlist'),
    url(r'^questiondetail/(?P<question_id>[0-9]+)/$', views.questiondetail, name='questiondetail'),
    url(r'^contact/$', views.contactus),
    url(r'^newquestion/$', views.newquestion, name='newquestion'),
    url(r'^search/$', views.search, name='search'),
    url(r'^mainsearch/$', views.mainsearch, name='mainsearch'),
    url(r'^searchpage/$', views.searchpage, name='searchpage'),
    url(r'^addsuggestion_ajax/$', views.addsuggestion_ajax, name='addsuggestion_ajax'),
    url(r'^votesuggestion/$', views.votesuggestion, name="votesuggestion"),
    url(r'^ratesuggestion/$', views.ratesuggestion, name="ratesuggestion"),
    url(r'^settingbutton/$', views.settingbutton, name="settingbutton")
]