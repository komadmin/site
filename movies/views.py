from django.shortcuts import get_object_or_404
from movies.models import Crew, ContactUs, Question, Suggestion
from django.http import HttpResponseRedirect
from movies.forms import ContactForm, NewQuestionForm, RateSuggestion
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm


def getcharacter(actorset, movie):
    actorset = list(actorset)
    for ii in range(0, len(actorset)):
        actorset[ii].character = actorset[ii].crewcredit_set.filter(movie=movie).first().character
    return actorset


def underconstruction(request):
    return HttpResponse("This site is under construction")


def listmovies(request):
    movie_list = Movie.objects.all().order_by('-imdb_votes')[0:100]
    return render(request, 'movies/index.html', dict(movie_list=movie_list))


# movie_id=13434
def moviedetail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/moviedetail.html', dict(movie=movie))


def actordetail(request, actor_id):
    actor = get_object_or_404(Crew, pk=actor_id)
    return render(request, 'movies/actordetail.html', dict(actor=actor))


def listactors(request):
    res = Crew.objects.filter(job='a').order_by('-imdb_comp')[0:100]
    context = dict(actor_list=res)
    return render(request, 'movies/actorlist.html', context)


def listdirectors(request):
    res = Crew.objects.filter(job="d").order_by('-imdb_comp')[0:100]
    context = dict(director_list=res)
    return render(request, 'movies/directorlist.html', context)


def questionlist(request):
    context = dict(question_list=Question.objects.all()[0:100])
    return render(request, 'movies/questionlist.html', context)


def newquestion(request):
    if not request.user.is_authenticated():
        return render(request, 'movies/newquestion.html', {'form': []})

    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            # .get gets the object directly whereas .filter gets a query set (which I think is always a list)
            u = User.objects.get(username=request.user.username)
            q = Question(question_text=form.cleaned_data["question_short"], user=u)
            q.save()

            return HttpResponseRedirect(reverse('movies:questiondetail', kwargs=dict(question_id=q.pk)))
    else:
        form = NewQuestionForm()

    return render(request, 'movies/newquestion.html', {'form': form})


def search(request):
    if request.method == 'GET':
        s = request.GET['searchtext']
        qid = request.GET['qid']
        if len(s) == 0:
            r = list()
        else:
            # r = Movie.objects.filter(title__istartswith=s).order_by('-imdb_rating')[0:10]
            # if len(r) < 10:
            r = Movie.objects.filter(title__icontains=s).order_by('-imdb_votes')[0:10] # [0:10-len(r)]
            # r = list(r) + list(rc)
            q = Question.objects.get(pk=qid)
            sugglist = [s.answer.pk for s in q.suggestion_set.all()]
            for ii in range(0, len(r)):
                name = list()
                res = r[ii].crewcredit_set.order_by('order')[0:2]
                for a in res:
                    name.append(a.crew.name)

                r[ii].actor_list = ', '.join(name)
                if r[ii].pk in sugglist:
                    r[ii].inlist = True

        return render(request, 'movies/searchresults.html', {'results': r})


def preprocess_sugglist(r):
    for ii in range(0, len(r)):
        name = list()
        answer = r[ii].answer
        res = answer.crew_set.filter(job="a").order_by('-crewcredit__order')[0:4]

        if not answer.youtubeid:
            y = youtube_search(answer.title + " trailer " + str(answer.date.year), 1)
            answer.youtubeid = y["id"]["videoId"]
            answer.save()



        r[ii].answer = answer

    return r


def questiondetail(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    r = q.suggestion_set.all().order_by("-vote")
    r = preprocess_sugglist(r)
    return render(request, 'movies/question_detail.html', {'q': q, 'current_suggestion_list': r})


def addsuggestion_ajax(request):
    if not request.user.is_authenticated():
        return HttpResponse('You are not logged in')
    if request.method == 'POST':
        form = AddSuggestion(request.POST)
    elif request.method == 'GET':
        form = AddSuggestion(request.GET)

    if form.is_valid():
        m = Movie.objects.get(pk=int(form.cleaned_data['mid']))
        q = Question.objects.get(pk=int(form.cleaned_data['qid']))
        u = User.objects.get(username=request.user.username)
        if len(q.suggestion_set.all().filter(answer=m.pk)) == 0:
            s = Suggestion(user=u, question=q, answer=m, reason=form.cleaned_data["reason"])
            s.save()

            # now return answer list
            r = q.suggestion_set.all()
            r = preprocess_sugglist(r)

        #   Could put extra code here to group and score suggestions etc.
        else:
            r = []

        return render(request, 'movies/addsuggestion_ajax.html', {'results': r})
    else:
        return HttpResponse("Form was not valid")



def votesuggestion(request):
    if not request.user.is_authenticated():
        return HttpResponse('You are not logged in')
    if request.method == 'POST':
        v = VoteOnSuggestion(request.POST)
    else:
        v = VoteOnSuggestion(request.GET)

    if v.is_valid():
        pk = int(v.data["suggid"])
        s = Suggestion.objects.get(pk=pk)
        if s.votefrom.filter(username=request.user.username):
            return HttpResponse('<span class="sugglist_vote_failed">%s<span>' % s.vote)
        if int(v.data["vote"]) == 1:
            s.vote = s.vote + 1
            s.votefrom.add(request.user)
            s.save()

        # elif v.cleaned_data["vote"] == 2:
        #     Suggestion.objects.get(pk=v.cleaned_data("suggid")).update(vote=F('vote') - 1)
        return HttpResponse('<span class="sugglist_vote_success">%s<span>' % s.vote)


def ratesuggestion(request):
    if not request.user.is_authenticated():
        return HttpResponse('You are not logged in')
    if request.method == 'POST':
        v = RateSuggestion(request.POST)
    else:
        v = RateSuggestion(request.GET)

    if v.is_valid():
        pk = int(v.data["suggid"])
        s = Suggestion.objects.get(pk=pk)
        q = Question.objects.get(pk=s.question.pk)
        if request.user.pk is not q.user.pk:
            return HttpResponse('Error: WRONG USER %s: %s' % (request.user.username, q.user.username))

        s.op_rating = v.data["rating"]
        s.op_message = v.cleaned_data["opcomment"]
        s.save()

        return HttpResponse(v.cleaned_data["opcomment"])
    else:
        return HttpResponse(v.errors)


def searchpage(request):
    return render(request, 'movies/searchpage.html', {'n': ''})


def user_register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/accounts/logout/')
    # if a GET (or any other method) we'll create a blank form
    else: form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST) # instantiate with data
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)

            c = ContactUs(subject=subject, message=message, sender=sender, recipients=recipients)
            c.save()
            return HttpResponseRedirect('/movies/movielist')

    else: form = ContactForm() # instantiate blank
    return render(request, 'movies/contactexample.html', {'form': form})



def preprocess_sugglist(r):
    for ii in range(0, len(r)):
        name = list()
        answer = r[ii].answer
        res = answer.crew_set.filter(job="a").order_by('-crewcredit__order')[0:4]
        for a in res:
            name.append(a.name)

        answer.actor_list = ', '.join(name)

        d = answer.crew_set.filter(job="d").order_by('-crewcredit__order')[0:2]
        name = list()
        for n in d:
            name.append(n.name)

        answer.director = ', '.join(name)

        if not answer.youtubeid:
            y = youtube_search(answer.title + " trailer " + str(answer.date.year), 1)
            answer.youtubeid = y["id"]["videoId"]
            answer.save()

        r[ii].answer = answer

    return r



from movies.similarviews import *

#
#
# mv = Movie.objects.annotate(
#     comp=ExpressionWrapper(F('imdb_votes') + F('imdb_rating'), output_field=FloatField()))
#
# mv = mv.order_by('-comp')
#
# print [m.comp for m in mv[1:10]]
