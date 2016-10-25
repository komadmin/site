from apiclient.discovery import build
from siteroot.local_settings import DEVELOPER_KEY
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(q="google", max_results=1):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=q,
    part="id",
    maxResults=max_results
  ).execute()

  for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
          id = search_result["id"]["videoId"]

  return search_result

# y = youtube_search("Interstellar trailer", 1)