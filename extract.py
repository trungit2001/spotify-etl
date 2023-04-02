import requests
import pandas as pd

from oauth import get_access_token
from datetime import datetime, timedelta

token = get_access_token()


def retrieve_data() -> pd.DataFrame:
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    user_params = {
        "limit": 50,
        "after": yesterday_unix_timestamp
    }

    # Download all song you've listened in the last 24 hours
    res = requests.get(
        url="https://api.spotify.com/v1/me/player/recently-played",
        params=user_params,
        headers=user_headers
    )
    
    if res.status_code != 200:
        raise Exception("Can't get recently played songs")
    
    data = res.json()
    songs_name = []
    artists_name = []
    played_at = []
    timestamps = []

    for song in data["items"]:
        songs_name.append(song["track"]["name"])
        artists_name.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])
        timestamps.append(song["played_at"][:10])

    songs = {
        "songs_name": songs_name,
        "artists_name": artists_name,
        "played_at": played_at,
        "timestamps": timestamps
    }

    song_df = pd.DataFrame(songs, columns=songs.keys())

    return song_df
