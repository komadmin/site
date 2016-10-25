from django.shortcuts import render
from movies.models import Movie, SimilarMovieRel
from django.http import HttpResponse
from movies.forms import AddSimilar, VoteOnSuggestion
from django.contrib.auth.models import User
from django.db.models import ExpressionWrapper, F, FloatField
from movies.lib.youtube_idonly import youtube_search
# import os, wget
# from PIL import Image
# from resizeimage import resizeimage


def preprocess_simlist(r):
    for ii in range(0, len(r)):
        l = r[ii].linkto
        name = list()
        res = l.crew_set.filter(job="a").order_by('-crewcredit__order')[0:4]
        for a in res:
            name.append(a.name)

        l.actor_list = ', '.join(name)

        d = l.crew_set.filter(job="d").order_by('-crewcredit__order')
        name = list()
        for n in d:
            name.append(n.name)

        l.director = ', '.join(name)

        if not l.youtubeid:
            y = youtube_search(r[ii].linkto.title + " trailer " + str(l.date.year), 1)
            try:
                l.youtubeid = y["id"]["videoId"]
                l.save()
            except:
                pass

        # SAVE POSTER IN SMALL
        # if not r[ii].linkto.postersaved:
        #     os.chdir("/home/darren/websites/komend/data/images/")
        #     url = 'http://ia.media-imdb.com/images/M/MV5BMTQ2NzkzMDI4OF5BMl5BanBnXkFtZTcwMDA0NzE1NA@@._V1_SX300.jpg'
        #     filename = wget.download(url)
        #     fn, ext = os.path.splitext(filename)
        #     fnsmall = fn + '_small' + ext
        #     if not os.path.exists(fnsmall):
        #         with open(filename, 'r+b') as f:
        #             with Image.open(f) as image:
        #                 cover = resizeimage.resize_cover(image, [136, 200])
        #                 cover.save(fnsmall, image.format)

    return r



def similarmoviessimple(request, movie_id):
    id = movie_id
    m = Movie.objects.get(pk=id)
    create_similar_links(m)
    s = SimilarMovieRel.objects.filter(linkfrom=m).order_by('-votes', '-linkfrom__imdb_rating')
    return render(request, 'movies/similar/similarmoviessimple.html', {'similar_list': s, 'link_from': m})



def similarmovies(request, movie_id):
    id = movie_id
    m = Movie.objects.get(pk=id)
    create_similar_links(m)
    s = SimilarMovieRel.objects.filter(linkfrom=m).order_by('-votes', '-linkto__imdb_rating')
    s = preprocess_simlist(s)
    return render(request, 'movies/similar/similarmovies.html', {'similar_list': s, 'm': m})



def create_similar_links(m):
    # if m.similar.first():
        # return 1
    t = m.movietags_set.filter(type='t').order_by('-n')
    mf = Movie.objects
    for tag in t:
        mf = mf.filter(movietags__tag=tag)
    mf = mf.annotate(comp=ExpressionWrapper(F('imdb_votes') * F('imdb_rating'), output_field=FloatField()))
    mf = mf.order_by('-comp')[0:20]
    ind = 0
    for r in mf:
        if SimilarMovieRel.objects.filter(linkfrom=m, linkto=r, basedon='tmain'):
            continue
        if r.imdb_id == m.imdb_id:
            continue
        s = SimilarMovieRel(linkfrom=m, linkto=r, basedon='tmain', score=ind, votes=0)
        ind += 1
        s.save()
    return 1



def votesimilar(request):
    if not request.user.is_authenticated():
        return HttpResponse('You are not logged in')
    if request.method == 'POST':
        v = VoteOnSuggestion(request.POST)
    else:
        v = VoteOnSuggestion(request.GET)

    if v.is_valid():
        pk = int(v.data["simid"])
        s = SimilarMovieRel.objects.get(pk=pk)
        if not request.user.pk == 1:
            if s.votefrom.filter(username=request.user.username):
                return HttpResponse('<span class="simlist_vote_failed">%s<span>' % s.votes)
        if int(v.data["vote"]) == 1:
            s.votes = s.votes + 1
            s.votefrom.add(request.user)
            s.save()

        return HttpResponse('<span class="simlist_vote_success">%s<span>' % s.votes)



def addsimilar_ajax(request):
    if not request.user.is_authenticated():
        return HttpResponse('You are not logged in')
    if request.method == 'POST':
        form = AddSimilar(request.POST)
    elif request.method == 'GET':
        form = AddSimilar(request.GET)

    if form.is_valid():
        linkto = Movie.objects.get(pk=int(form.cleaned_data['linkto']))
        linkfrom = Movie.objects.get(pk=int(form.cleaned_data['linkfrom']))
        u = User.objects.get(username=request.user.username)
        if not linkfrom.similar.filter(pk=linkto.pk):
            s = SimilarMovieRel(user=u, linkfrom=linkfrom, linkto=linkto, reason=form.cleaned_data["reason"], votes=1, score=0)
            s.save()

            # now return new similar list
            r = SimilarMovieRel.objects.filter(linkfrom=linkfrom).order_by('-votes', '-linkto__imdb_rating')
            r = preprocess_simlist(r)

        #   Could put extra code here to group and score suggestions etc.
        else:
            r = []

        return render(request, 'movies/similar/addsimilar_ajax.html', {'results': r})
    else:
        return HttpResponse(form.errors)



def search(request):
    if request.method == 'GET':
        s = request.GET['searchtext']
        mid = request.GET['linkfrom']
        if len(s) == 0:
            r = list()
        else:
            r = Movie.objects.filter(title__icontains=s).order_by('-imdb_votes')[0:10]
            m = Movie.objects.get(pk=mid)
            linktolist = [s.pk for s in m.similar.all()]
            linktolist.append(m.pk)
            for ii in range(0, len(r)):
                name = list()
                res = r[ii].crewcredit_set.order_by('order')[0:2]
                for a in res:
                    name.append(a.crew.name)

                r[ii].actor_list = ', '.join(name)
                if r[ii].pk in linktolist:
                    r[ii].inlist = True

        return render(request, 'movies/searchresults.html', {'results': r})