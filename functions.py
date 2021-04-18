import tkinter as tk
from threading import Thread
from const import *
import pytube
import os
import re


def download_video(url='', folder=''):
    """Download video function and make dir if not exist"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    pytube.YouTube(url).streams.first().download(folder)


def download_playlist(url='', folder=''):
    """Download playlist function and make dir if not exist"""
    youtube_stream_audio = '140'  # Download juste the audio
    playlist = pytube.Playlist(url)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    # physically downloading the audio track
    for video in playlist.videos:
        audio_stream = video.streams.get_by_itag(int(youtube_stream_audio))
        audio_stream.download(output_path=folder)


def download(mode=1, url='', folder=''):
    """Call playlist or video download"""
    # Video download
    if mode == 1:
        thread = Thread(target=download_video, args=(url, folder))
        thread.start()
    elif mode == 2:
        thread = Thread(target=download_playlist, args=(url, folder))
        thread.start()


def draw_component(window):
    # Playlist
    label = tk.Label(window, text="Télecharger une playlist:", bg=BG_COLOR, font=("Arial", 20, 'bold', 'underline'),
                     fg="white")
    label.pack(pady=60)

    playlist_url = tk.Entry(window, width=30, font=("Arial", 15, 'bold'), justify="center")
    playlist_url.pack()

    playlist_button = tk.Button(window, text="Download Playlist", width=30, command=lambda: download(2,
                                                                                                     playlist_url.get(),
                                                                                                     DOWNLOAD_FOLDER))
    playlist_button.pack(pady=10)

    # Video
    label = tk.Label(window, text="Télecharger une vidéo:", bg=BG_COLOR, font=("Arial", 20, 'bold', 'underline'),
                     fg="white")
    label.pack(pady=60)

    video_url = tk.Entry(window, width=30, font=("Arial", 15, 'bold'), justify="center")
    video_url.pack()

    playlist_button = tk.Button(window, text="Download Video", width=30, command=lambda: download(1,
                                                                                                  video_url.get(),
                                                                                                  DOWNLOAD_FOLDER))
    playlist_button.pack(pady=10)
