from movies.models import Movie, Actor, Question, Suggestion
import json
from datetime import date
from django.contrib.auth.models import User
import csv


fname = "/home/darren/websites/komend/data/omdbMovies.txt"

import codecs
f = codecs.open(fname, 'r', 'ISO-8859-1')
l = f.readline().replace('\r\n', '')
names = l.split('\t')

#
ldata = 0;
for line in f:
    # c = ci2/ci
    l = line.replace('\r\n', '').split('\t')
    d = {names[ii]: l[ii] for ii in range(0, len(l))}
    if len(d) == 21:
        fld = 'Genre'
        if len(d[fld]) > ldata:
            ldata = len(d[fld])
            ex = d[fld]
        # if len(d['Metacritic']) > 0:
            # print(d['Metacritic'])
        # print(d['imdbRating'])
print(ldata)
print(ex)
