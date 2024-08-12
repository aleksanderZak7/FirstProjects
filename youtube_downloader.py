"""
How to run the YouTube Video Downloader:

This program is used for downloading videos from a specified URL using the yt_dlp library.

Usage:
  python downloader.py -i <VIDEO_URL> -o <OUTPUT_PATH> [-q <QUALITY>] [--cookies <COOKIES_PATH>]

Options:
  -i, --input     (required) URL of the video to download.
  -o, --output    (required) Path where the video file will be saved.
  -q, --quality   (optional) Quality of the video to download. Can be "best", "worst", "bestaudio", "bestvideo". Default is "best".
  --cookies       (optional) Path to a cookies file for authentication.

Example:
  python youtube_downloader.py -i https://www.youtube.com/watch?v=dQw4w9WgXcQ -o ./videos/my_video.mp4
"""

import os
import yt_dlp
import logging
import argparse
import validators

logging.basicConfig(level=logging.INFO)

class YoutubeDownloader:
    """
    Class for downloading YouTube videos using yt_dlp.

    Attributes:
        error (str): Error message if any download issue occurs.
        _input_link (str): URL of the video to download.
        _output_file_path (str): Path where the video file will be saved.
        _quality (str): Quality of the video to download (e.g., "best", "worst").
        _cookies_file (str): Path to a cookies file for authentication.
    """

    def __init__(self, input_link, output_file_path, quality, cookies_file):
        """
        Initializes the downloader with necessary parameters.

        Parameters:
            input_link (str): URL of the video to download.
            output_file_path (str): Path where the video file will be saved.
            quality (str): Quality of the video to download (e.g., "best", "worst").
            cookies_file (str): Path to a cookies file for authentication.
        """
        self.error = None
        self._input_link = input_link
        self._output_file_path = output_file_path
        self._quality = quality
        self._cookies_file = cookies_file

    def set_download_params(self):
        """
        Validate and set download parameters.

        Returns:
            bool: True if parameters are valid, False otherwise.
        """
        if not validators.url(self._input_link):
            self.error = "Error: Invalid URL format."
            return False

        output_dir = os.path.dirname(self._output_file_path)
        if not os.path.isdir(output_dir):
            self.error = f"Error: Output directory '{output_dir}' does not exist."
            return False

        if os.path.isfile(self._output_file_path):
            logging.warning("Warning: Output file already exists and will be overwritten!")

        return True

    def run_download(self):
        """
        Execute the video download process.
        """
        try:
            ydl_opts = {'format': self._quality, 'outtmpl': self._output_file_path, 'cookiefile': self._cookies_file }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logging.info(f"Downloading video from: {self._input_link}")
                ydl.download([self._input_link])
                logging.info(f"Video downloaded successfully and saved to {self._output_file_path}")  
        except yt_dlp.utils.DownloadError as e:
            logging.error(f"Download error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Download video from URL.')
    parser.add_argument('--cookies', help='Path to a cookies file for authentication.')
    parser.add_argument('-i', '--input', required=True, help='URL of the video to download.')
    parser.add_argument('-o', '--output', required=True, help='Path where the video file will be saved.')
    parser.add_argument('-q', '--quality', default='best', help='Quality of the video to download (e.g., "best", "worst", "bestaudio", "bestvideo").')
    args = parser.parse_args()

    downloader = YoutubeDownloader(args.input, os.path.abspath(args.output), args.quality, args.cookies)
    if downloader.set_download_params():
        downloader.run_download()
    else:
        logging.error(downloader.error)

if __name__ == '__main__':
    main()