import os
import flask
import requests
import asyncio
from flask import Flask, redirect, url_for, session, jsonify, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from video_archiver import fetch_videos, download_video

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SERVICE_NAME = "youtube.googleapis.com"
API_VERSION = "v2"
SECRET_KEY = "REPLACE ME - this value is here as a placeholder."

app = Flask(__name__)
app.secret_key = SECRET_KEY


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test")
def test_api_request():
    if "credentials" not in session:
        return redirect(url_for("authorize"))

    credentials = Credentials(**session["credentials"])
    session["credentials"] = credentials_to_dict(credentials)

    with open("token.json", "w") as token:
        token.write(credentials.to_json())

    return jsonify({"message": "Authentication successful!"})


@app.route("/authorize")
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        SCOPES,
        redirect_uri=url_for("oauth2callback", _external=True),
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )

    session["state"] = state
    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    state = session["state"]
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        SCOPES,
        state=state,
        redirect_uri=url_for("oauth2callback", _external=True),
    )
    flow.fetch_token(authorization_response=flask.request.url)

    session["credentials"] = credentials_to_dict(flow.credentials)

    return redirect(url_for("test_api_request"))


@app.route("/revoke")
def revoke():
    if "credentials" not in session:
        return redirect(url_for("authorize"))

    credentials = Credentials(**session["credentials"])
    requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    return (
        "Credentials successfully revoked."
        if credentials.valid
        else "An error occurred."
    )


@app.route("/clear")
def clear_credentials():
    try:
        del flask.session["key_name"]
    except KeyError:
        pass
    return "Credentials have been cleared."


@app.cli.command("download-playlist")
def download_playlist():
    api_key = os.getenv("YOUTUBE_API_KEY", "")
    playlist_id = os.getenv("YOUTUBE_PLAYLIST_ID", "")

    if not api_key or not playlist_id:
        print("API key or playlist ID not provided.")
        return

    async def async_wrapper():
        videos = fetch_videos(playlist_id)
        await asyncio.gather(*(download_video(url, title) for url, title in videos))

    # Run the async wrapper in the event loop
    asyncio.run(async_wrapper())


if __name__ == "__main__":
    app.run("localhost", 8080, debug=True)
