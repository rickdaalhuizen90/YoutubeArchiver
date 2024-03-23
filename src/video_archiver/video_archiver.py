import os
import re
import subprocess
import asyncio
import logging
from typing import Generator, Tuple
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

APIKey = str
PlaylistID = str
VideoURL = str
VideoTitle = str


def get_authenticated_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        raise FileNotFoundError("token.json not found. Please authenticate manually.")

    return build("youtube", "v3", credentials=creds)


def fetch_videos(
    playlist_id: PlaylistID,
) -> Generator[Tuple[VideoURL, VideoTitle], None, None]:
    youtube = get_authenticated_service()
    try:
        request = youtube.playlistItems().list(
            part="snippet", playlistId=playlist_id, maxResults=20
        )
        response = request.execute()
    except HttpError as e:
        print(f"Failed to fetch videos: {e}")
        return

    for item in response.get("items", []):
        video_id: str = item["snippet"]["resourceId"]["videoId"]
        video_title: str = item["snippet"]["title"]

        yield f"https://www.youtube.com/watch?v={video_id}", video_title

async def download_video(url: VideoURL, title: VideoTitle, folder: str = "./downloads") -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        file_name = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        file_name = re.sub(r'\s+', '_', file_name)

        if os.path.exists(f"{folder}/{file_name}.mp4"):
            print(f"{title} already exists")
            return

        print(f"Downloading video: {title}...")

        process = await asyncio.create_subprocess_exec(
            "yt-dlp", "-o", os.path.join(folder, f"{file_name}.%(ext)s"), url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            print(f"Failed to download video {title}: {stderr.decode()}")
    except Exception as e:  # It's generally a good idea to catch specific exceptions
        print(f"Failed to download video {title}: {e}")