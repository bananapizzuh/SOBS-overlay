# SOBS-Overlay
A spotify overlay made for OBS studio using spotipy and flask.

![example.gif](example.gif)

## How to use
- Clone this repository and either run `pipenv install` or `pip install requirements.txt`.
- Generate a spotify developer client ID and client Secret for the web api [here](https://developer.spotify.com/dashboard).
- Put them in a .env file in the same directory as the application, it should look like this:
    ```
    SPOTIPY_CLIENT_ID="{Your ID Here}"
    SPOTIPY_CLIENT_SECRET="{Your Secret Here}"
    ```
    (Do not forget to remove the brakets as you put your ID and secret there)  
- Then run `pipenv run flask run` or just `flask run` if you aren't using a virtual environment.
- Go to http://127.0.0.1:5000/ to authenticate with spotify, then add it as a browser source in OBS.
- Set the width to 450 and height to 110 and you are good to go!