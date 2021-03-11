from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

SPOTIFY_CLIENT_ID = "YOUR CLIENT ID HERE"
SPOTIFY_CLIENT_SECRET = "YOUR CLIENT SECRET HERE"
SPOTIPY_REDIRECT_URI = "YOUR REDIRECT URI HERE"





date = input("Which date would you like to travel to? (In YYYY-MM-DD format)")
URL = "https://www.billboard.com/charts/hot-100/" + date

response=requests.get(URL)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")
songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
artists=soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")
song_list=[]
artist_list=[]
for song in songs:
    to_add = song.contents
    song_list.append(to_add)
print(song_list)
for artist in artists:
    to_add1 = artist.contents
    artist_list.append(to_add1)
print(artist_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uri_list=[]
for song in song_list:
    uri = sp.search(song)["tracks"]["items"][0]["uri"]
    song_uri_list.append(uri)
print(song_uri_list)

playlist = sp.user_playlist_create(user_id,f"{date} Billboard 100",public=False,collaborative=False)
playlist_id = playlist["id"]

sp.user_playlist_add_tracks(user_id,playlist_id,song_uri_list)
