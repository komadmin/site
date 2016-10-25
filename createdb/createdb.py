##
import tmdbsimple as tmdb
import time
# from urllib.request import Request, urlopen
from requests.exceptions import HTTPError
import json
import os

tmdb.API_KEY = 'd7d0d2bfc8b2379fedded9dbd1f356b5'

fname = '/home/darren/websites/komend/data/omdbMovies.txt'

tt = list()
# with open(fname, encoding='ISO-8859-1') as o:
with open(fname) as o:
    for line in o:
        tt.append((line.split('\t')[1]))

o.close()

##

movie = tmdb.Movies(tt[1]).info()


fname = '/home/darren/websites/komend/data/tmdbJSON.txt'
if os.path.exists(fname):
    os.remove(fname)

##

ind = 1
with open(fname, 'w') as f:
    for id in tt:
        if ind < 10:
            try:
                movie = tmdb.Movies(id).info()
                f.write(json.dumps(movie) + "\n")
                # Wait for 5 seconds
                print("%s success" % id)
                time.sleep(1/20)
            except HTTPError:
                print("error")


##
#
# fname = '/home/darren/websites/komend/data/tmdbJSON.txt'
#
# with open(fname, 'r') as f:
#     for line in f:
#         print(line)
#         time.sleep(1)