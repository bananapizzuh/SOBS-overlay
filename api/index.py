import html
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, redirect, session, request
import requests
import os
from datetime import datetime, timezone
import base64
from urllib.parse import urlencode
import random
import string

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")


app = Flask(__name__)
app.secret_key = os.urandom(32)


def generate_random_string(length):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def check_auth():
    try:
        if session["code"] or session["code"]:
            return True
    except:
        return False


def get_token(code=None, redirect_uri=redirect_uri, refresh_token=False):
    if not check_auth():
        return None

    time_acquired = datetime.now(timezone.utc)
    if refresh_token:
        data = {
            "refresh_token": code,
            "grant_type": "refresh_token",
        }
    else:
        data = {
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}",
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token", data=data, headers=headers
    )
    response = response.json()
    response["time_acquired"] = time_acquired

    return response


def get_auth_url():
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-read-currently-playing user-read-playback-state",
        "state": generate_random_string(16),
    }

    return f"https://accounts.spotify.com/authorize?{urlencode(params)}"


@app.route("/callback")
def callback():
    session["code"] = request.args.get("code")
    state = request.args.get("state")

    if state == None:
        return redirect("/")

    session["token"] = get_token(session["code"])
    return redirect("/embed")


@app.route("/update")
def update():
    if not check_auth():
        return redirect("/")

    if (
        session["token"]["time_acquired"] - datetime.now(timezone.utc)
    ).total_seconds() > 3600:
        session["token"] = get_token(session["code"], refresh_token=True)

    headers = {
        "Authorization": f"Bearer {session['token']['access_token']}",
    }

    current_track = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing", headers=headers
    ).json()

    if current_track is not None and "item" in current_track:
        track_name = html.unescape(current_track["item"]["name"])
        artists = [html.unescape(x) for x in current_track["item"]["artists"]]
        album_cover = current_track["item"]["album"]["images"][0]["url"]
        progress = current_track["progress_ms"]
        duration = current_track["item"]["duration_ms"]

    else:
        track_name = ""
        artists = []
        album_cover = ""
        progress = 0
        duration = 0

    response = jsonify(
        {
            "track_name": track_name,
            "artists": artists,
            "album_cover": album_cover,
            "progress": progress,
            "duration": duration,
        }
    )

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/embed")
def embed():

    return render_template("embed.html")


@app.route("/")
def index():
    if check_auth():
        return redirect("/embed")
    session["code"] = None
    session["token"] = None
    return redirect(get_auth_url())


if __name__ == "__main__":
    app.run()
