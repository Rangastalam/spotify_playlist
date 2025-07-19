import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

CLIENT_ID="your client id"
CLIENT_SECRET="your client secret"
REDIRECT_URI="http://example.com"


scope = "user-library-read"
os.environ["SPOTIPY_CLIENT_ID"]=CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"]=CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"]=REDIRECT_URI


date=input("Which date you want to travel to? Type the date in this format YYYY-MM-DD: ")
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}


try:
    response=requests.get(f"https://www.billboard.com/charts/hot-100/{date}/",headers=header)
    response.raise_for_status()
except requests.exceptions.HTTPError:
    print("Error Occurred !!!Enter Date in Proper format!!!!")
else:
    webcontent=response.text
    soup=BeautifulSoup(webcontent,"html.parser")
    songs_list=soup.select("li>h3#title-of-a-story.c-title")

    songs_list=[song_element.getText().strip() for song_element in songs_list]
    print(songs_list)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        show_dialog=True,
        cache_path="token.txt",
        username="",
))
user_details=sp.current_user()
print(user_details)


song_uris = []
year = date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(song_uris)
playlist_id=sp.user_playlist_create(user_details["id"],f"Top_100_songs_{date}", public=False)

sp.playlist_add_items(playlist_id["id"],song_uris)







