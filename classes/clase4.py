import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import glob
import pandas as pd


api_client_id = "afb9df263712418ebf70719331e55197"
api_client_secret = "d93d1ad5441447e58e1e21cadc6290b1"

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(api_client_id, api_client_secret))

playlist_list = ("37i9dQZF1DXaxEKcoCdWHD", "37i9dQZEVXbNFJfN1Vw8d9")


def get_playlist(playlist, offset):
    resposta = spotify.playlist_items(playlist, offset=offset)
    with open(f'{playlist}-{offset}.json', 'w', encoding='utf-8') as f:
        json.dump(resposta, f, ensure_ascii=False, indent=4)

    if resposta["next"] == None:
        print("Final")
        pass
    else:
        offset = offset + 100
        print("nova peticio")
        get_playlist(playlist, offset)


for playlist in playlist_list:
    offset = 0
    get_playlist(playlist, offset)


files = glob.glob("*.json")
list_tracks = []

for file in files:
    with open(file, encoding="utf8") as f:
        d = json.load(f)
        print(d)
        tracks = d ["items"]
        for track in tracks:
            track_dict={}
            track_dict['name'] = track["track"]["name"]
            track_dict ['artist_name'] = track["track"]["artists"][0]['name']
            track_dict['duracio_ms'] = track["track"]["duration_ms"]
            track_dict['duracio_min'] = round(track["track"]["duration_ms"]/1000/60, 2)
            track_dict['popularity'] = track["track"]["popularity"]

            list_tracks.append(track_dict)

df = pd.DataFrame.from_dict(data)
df.to_csv("output.csv", index= False, sep=";")