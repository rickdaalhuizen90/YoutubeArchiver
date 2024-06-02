import os
import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Download videos from YouTube channels listed in a CSV file.")
    parser.add_argument('--csv', type=str, required=True, help='Path to the CSV file containing channel names and URLs.')
    parser.add_argument('--output', type=str, required=True, help='Directory where videos will be downloaded.')

    args = parser.parse_args()
    csv_file = args.csv
    
    output_dir = Path(args.output).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    CMD = "yt-dlp"

    if os.system(f"command -v {CMD} > /dev/null") != 0:
        print(f"{CMD} could not be found, please install it first.")
        sys.exit(1)

    if not os.path.isfile(csv_file):
        print(f"CSV file '{csv_file}' not found.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    PRIVATE_CHANNEL_URL = "https://www.youtube.com/playlist?list=WL"
    PRIVATE_CHANNEL_NAME = "WatchLater"
    PRIVATE_CHANNEL_OUTPUT_DIR = os.path.join(output_dir, PRIVATE_CHANNEL_NAME)

    os.makedirs(PRIVATE_CHANNEL_OUTPUT_DIR, exist_ok=True)

    print("Downloading videos from your private channel")
    os.system(f"{CMD} --cookies-from-browser chrome --download-archive '{PRIVATE_CHANNEL_OUTPUT_DIR}/downloaded.txt' -o '{PRIVATE_CHANNEL_OUTPUT_DIR}/%(title)s.%(ext)s' '{PRIVATE_CHANNEL_URL}'")

    def download_videos(channel_name, channel_url):
        channel_output_dir = os.path.join(output_dir, channel_name)
        os.makedirs(channel_output_dir, exist_ok=True)
        print(f"Downloading videos for channel: {channel_name}")
        os.system(f"{CMD} --download-archive '{channel_output_dir}/downloaded.txt' -o '{channel_output_dir}/%(title)s.%(ext)s' '{channel_url}'")

    with open(csv_file, "r") as file:
        for line in file:
            parts = line.strip().split(",", 1)
            if len(parts) != 2:
                continue
            channel_name, channel_url = parts
            download_videos(channel_name, channel_url)

if __name__ == "__main__":
    main()
