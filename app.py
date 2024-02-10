import html
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, jsonify, Response

load_dotenv()
app = Flask(__name__)
spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        redirect_uri="http://localhost:5000/callback",
        scope="user-read-currently-playing",
    )
)


@app.route("/callback")
def callback():
    return "Callback received"


@app.route("/update")
def update():

    current_track = spotify.current_playback()
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


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
