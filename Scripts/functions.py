import tkinter as tk
from threading import Thread
from Scripts.const import DOWNLOAD_FOLDER, BG_COLOR
import json
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


def save_settings(data):
    with open("../Files/settings.json", "w") as f:
        json.dump(data, f, indent=4)


def get_settings():
    with open("../Files/settings.json", "r") as f:
        data = json.load(f)
    return data


def settings_window():
    print("window")


def draw_component(window):
    """Display tkinter component on window"""
    settings_button = tk.Button(window, text="Settings", width=15, command=lambda: settings_window())
    settings_button.pack(anchor="e")

    label_list = ["Download a video", "Download video", "Download a playlist", "Download playlist"]

    for i in range(2):
        title_label = tk.Label(window, text=label_list[i * 2], bg=BG_COLOR,
                               font=("Arial", 20, 'bold', 'underline'), fg="white")
        title_label.pack(pady=30)

        url_label = tk.Label(window, text="URL", bg=BG_COLOR, font=("Arial", 18, 'bold', 'underline'), fg="white")
        url_label.pack(pady=10)

        user_url = tk.Entry(window, width=30, font=("Arial", 15, 'bold'), justify="center")
        user_url.pack()

        playlist_button = tk.Button(window, text=label_list[i * 2 + 1], width=30,
                                    command=lambda button=i: download(button + 1, user_url.get(), DOWNLOAD_FOLDER))
        playlist_button.pack(pady=10)
