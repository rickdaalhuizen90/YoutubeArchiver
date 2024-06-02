# YouTube Archiver

YouTube Archiver is a tool designed to create offline backups of your favorite YouTube videos, ensuring they remain accessible even if they are removed from YouTube.

## Usage

1. Begin by copying the example channels CSV file to `channels.csv` and then update it with the channels you wish to archive.
   ```bash
   cp channels.example.csv channels.csv
   ```

2. Execute the script to commence archiving your YouTube videos.
    ```bash
    python yt-archiver.py
    ```

### Note:

- The script intelligently skips downloading videos that have already been archived. It maintains a record of downloaded videos in each channel's `downloaded.txt` file to prevent duplicates.
- Remember to periodically update the `channels.csv` file with any new channels you want to archive.

## License

This project is licensed under the MIT License - see the LICENSE.md file for more details.
