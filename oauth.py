import os
import json
import base64
import requests
import webbrowser
import time

from urllib.parse import urlencode
from dotenv import load_dotenv
from argparse import ArgumentParser

# load enviroment variable
load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
token_path = f"{os.path.expanduser('~')}/token.json"


def get_auth_code():
    url_auth = "https://accounts.spotify.com/authorize?"
    auth_headers = {
        "client_id": client_id,
        "scope": "user-read-recently-played",
        "response_type": "code",
        "redirect_uri": redirect_uri
    }

    print("Please login and approve app access to your account")
    webbrowser.open(url_auth + urlencode(auth_headers))


def get_auth_token(code: str):
    url_token = "https://accounts.spotify.com/api/token"
    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")
    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }

    start_time = time.time()
    res = requests.post(url_token, data=token_data, headers=token_headers)
    
    if res.status_code == 200:
        res = res.json()
        obj_data = {
            "token": res["access_token"],
            "expires_time": start_time + res["expires_in"]
        }
        
        with open(token_path, 'w', encoding="utf-8") as fp:
            json.dump(obj_data, fp, ensure_ascii=False)
            print("Get access token successfully")
    else:
        raise Exception("Can't authenticate")


def get_access_token() -> str:
    if os.path.exists(token_path):
        with open(token_path, 'r', encoding="utf-8") as fp:
            obj_data = json.load(fp)
            if obj_data["expires_time"] - time.time() > 0:
                return obj_data["token"]
    
    raise Exception("Can't get token, please login again")


if __name__ == "__main__":
    parser = ArgumentParser(description="This program helps to get 'code' and 'token' to access Spotify API")
    parser.add_argument("-l", "--login", action="store_true", help="Open web browser for login Spotify and get auth code")
    parser.add_argument("-c", "--code", default=str, help="Paste your auth code to get access token")

    args = parser.parse_args()
    
    if args.login:
        get_auth_code()
    
    elif args.code != None:
        get_auth_token(args.code)
