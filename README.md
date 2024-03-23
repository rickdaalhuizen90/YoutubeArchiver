# Video Archiver

Video Archiver is a Python tool designed to build an offline collection of your favorite YouTube videos, protecting them from potential deletions.

## Getting Started

These instructions will help you set up and run Video Archiver on your local machine using Docker.

### Prerequisites
Before downloading any videos, especially from private libraries, you must create API keys. Follow the instructions provided by Google to [register an application](https://developers.google.com/youtube/registering_an_application) and obtain your API keys.

### Build the Docker image:
```bash
docker build -t video-archiver:latest --no-cache .
```

### Authentication
Navigate to http://localhost:8080 and authenticate yourself. Ensure the "Authorized redirect URIs" in your Google project settings includes `http://localhost:8080/oauth2callback`, and "Authorized JavaScript origins" includes `http://localhost:8080`.

### Running the Docker Container
To run the script and start downloading videos from the specified YouTube playlist, execute:
```bash
docker run -p "8080:5000" --name video-archiver -d -v "$(pwd)/downloads:/usr/src/app/downloads" video-archiver:latest
```

### Downloading Videos
```bash
docker exec -it video-archiver flask download-playlist
```

## Environment Variables
- `YOUTUBE_API_KEY`: Your YouTube Data API v3 key.
- `YOUTUBE_PLAYLIST_ID`: The ID of the YouTube playlist from which you want to download videos.

Make sure to replace 'your_api_key_here' and 'your_playlist_id_here' with your actual YouTube API key and playlist ID.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.