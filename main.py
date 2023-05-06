import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy import SpotifyOAuth

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://example.com"

response_html = requests.get(URL).text
soup = BeautifulSoup(response_html, "html.parser")

song_names = []

rows = soup.find_all(class_="lrv-a-unstyle-list lrv-u-flex lrv-u-height-100p lrv-u-flex-direction-column@mobile-max")

for row in rows:
    song_names.append(row.find("h3").get_text().strip() + " " + row.find("span").get_text().strip())

print("Song names:\n")
print(song_names)

scope = "user-library-read playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI))

track_of_user = sp.current_user_saved_tracks()
print("Current user ID:")
print(sp.current_user()["id"])

uri_list = [sp.search(q=song_name, type="track")["tracks"]["items"][0]["uri"] for song_name in song_names]

print("URI list:\n")
print(uri_list)

new_playlist_name = date + " Billboard 100"
new_playlist = sp.user_playlist_create(user=sp.current_user()["id"], name=new_playlist_name, public=False, collaborative=False,
                        description="Created automatically using Musical time machine")

print("New playlist ID:\n")
print(new_playlist["id"])

sp.playlist_add_items(playlist_id=new_playlist["id"], items=uri_list, position=None)
