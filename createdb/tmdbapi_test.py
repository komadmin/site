from urllib.request import Request, urlopen
import json, codecs


headers = {
  'Accept': 'application/json'
}


request = Request('https://api.themoviedb.org/3/movie/550?api_key=d7d0d2bfc8b2379fedded9dbd1f356b5', headers=headers)
response_body = urlopen(request)
reader = codecs.getreader("utf-8")



obj = json.load(reader(response_body))

print(json.dumps(obj, indent=4))