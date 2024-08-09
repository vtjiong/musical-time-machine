import os
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()
# Getting top 100 songs from Billboard100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}").text
soup = BeautifulSoup(response, "html.parser")
raw_titles = soup.select(selector="li ul li h3")
song_names = [song.getText().strip() for song in raw_titles]

# OAuth using spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                               client_secret=os.getenv("CLIENT_SECRET"),
                                               redirect_uri="https://example.com",
                                               scope="playlist-modify-private",
                                               cache_path="token.txt",
                                               show_dialog=True))
user_id = sp.current_user()["id"]
song_uri = []
# Creating a list of the songs spotify uri
for track in song_names:
    try:
        queries = f"track={track} year={date.split("-")[0]}"
        uri = sp.search(q=queries, type='track')
        song_id = uri["tracks"]["items"][0]["id"]
        song_uri.append(song_id)
    except IndexError:
        print(f"{track} is not in the database")
# Creating the playlist and adding the song
playlist = f"{date}'s Billboard 100"
response = sp.user_playlist_create(user=user_id, name=playlist, public=False)
sp.playlist_add_items(playlist_id=response["id"], items=song_uri)
