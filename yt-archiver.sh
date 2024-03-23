#!/bin/bash

if ! command -v yt-dlp &> /dev/null; then
    echo "yt-dlp could not be found, please install it first."
    exit 1
fi

CSV_FILE="channels.csv"
OUTPUT_DIR="downloads"

if [ ! -f "$CSV_FILE" ]; then
    echo "CSV file '$CSV_FILE' not found."
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

download_videos() {
    local channel_name=$1
    local channel_url=$2
    local channel_output_dir="$OUTPUT_DIR/$channel_name"

    mkdir -p "$channel_output_dir"

    echo "Downloading videos for channel: $channel_name"
    yt-dlp --download-archive "$channel_output_dir/downloaded.txt" -o "$channel_output_dir/%(title)s.%(ext)s" "$channel_url"
}

while IFS=, read -r channel_name channel_url; do
    if [[ -z "$channel_name" || -z "$channel_url" ]]; then
        continue
    fi

    download_videos "$channel_name" "$channel_url"
done < "$CSV_FILE"

PRIVATE_CHANNEL_URL="https://www.youtube.com/playlist?list=WL"
PRIVATE_CHANNEL_NAME="WatchLater"
PRIVATE_CHANNEL_OUTPUT_DIR="$OUTPUT_DIR/$PRIVATE_CHANNEL_NAME"

mkdir -p "$PRIVATE_CHANNEL_OUTPUT_DIR"

echo "Downloading videos from your private channel"
yt-dlp --cookies-from-browser chrome --download-archive "$PRIVATE_CHANNEL_OUTPUT_DIR/downloaded.txt" -o "$PRIVATE_CHANNEL_OUTPUT_DIR/%(title)s.%(ext)s" "$PRIVATE_CHANNEL_URL"
