import tkinter as tk
from threading import Thread
from const import DOWNLOAD_FOLDER, BG_COLOR
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


def save_settings(color=BG_COLOR, folder=DOWNLOAD_FOLDER):
    """Save settings in a json files"""
    if color == "":
        color = BG_COLOR
    if folder == "":
        folder = DOWNLOAD_FOLDER

    data = {
        "background_color": color,
        "DOWNLOAD_FOLDER": folder
    }
    with open("../Files/settings.json", "w") as f:
        json.dump(data, f, indent=4)


def get_settings():
    """Load settings from json file and return it"""
    with open("../Files/settings.json", "r") as f:
        data = json.load(f)
    return data


def settings_window(bg_color):
    """Display settings window"""
    window = tk.Tk()
    window.minsize(720, 480)
    window.maxsize(720, 480)
    window.title('Settings')
    window['bg'] = bg_color

    title_label = ["Color (#fff)", "Folder path", "Apply change"]
    user_entry_list = []

    for i in range(2):
        text_label = tk.Label(window, text=title_label[i], bg=bg_color, font=("Arial", 18, 'bold', 'underline'),
                              fg="white")
        text_label.pack(pady=30)
        user_entry = tk.Entry(window, width=10 + 10 * i, font=("Arial", 15, 'bold'), justify="center")
        user_entry.pack()
        user_entry_list.append(user_entry)

    function_button = tk.Button(window, text=title_label[2], width=20,
                                command=lambda: save_settings(user_entry_list[0].get(), user_entry_list[1].get()))
    function_button.pack(pady=20)

    window.mainloop()


def draw_component(window, path, bg_color):
    """Display tkinter component on window"""
    settings_button_image = tk.PhotoImage(file="../Images/gear.png").subsample(2)
    settings_button = tk.Button(window, image=settings_button_image, command=lambda: settings_window(bg_color),
                                bg=bg_color, borderwidth=0, activebackground=bg_color)
    settings_button.image = settings_button_image
    settings_button.pack(anchor="e", pady=5, padx=5)

    label_list = ["Download a video", "Download video", "Download a playlist", "Download playlist"]
    user_entry = []
    for i in range(2):
        title_label = tk.Label(window, text=label_list[i * 2], bg=bg_color,
                               font=("Arial", 20, 'bold', 'underline'), fg="white")
        title_label.pack(pady=30)

        url_label = tk.Label(window, text="URL", bg=bg_color, font=("Arial", 18, 'bold', 'underline'), fg="white")
        url_label.pack(pady=10)

        user_url = tk.Entry(window, width=30, font=("Arial", 15, 'bold'), justify="center")
        user_url.pack()
        user_entry.append(user_url)

        playlist_button = tk.Button(window, text=label_list[i * 2 + 1], width=30,
                                    command=lambda button=i: download(button + 1, user_entry[button].get(), path))
        playlist_button.pack(pady=10)
