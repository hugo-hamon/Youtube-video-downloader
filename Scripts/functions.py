import tkinter as tk
from tkinter import ttk
from threading import Thread
from const import DOWNLOAD_FOLDER, BG_COLOR, INDEX_DOWNLOAD
import json
import pytube
import os
import re


def is_valid_color(color):
    regex = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    p = re.compile(regex)

    if color is None:
        return False

    if re.search(p, color):
        return True
    else:
        return False


def download_video(url=''):
    """Download video function and make dir if not exist"""
    data = get_settings()
    folder = data['DOWNLOAD_FOLDER']
    if not os.path.exists(folder):
        os.makedirs(folder)
    pytube.YouTube(url).streams.get_highest_resolution().download(folder)


def download_playlist(url=''):
    """Download playlist function and make dir if not exist"""
    data = get_settings()
    folder = data['DOWNLOAD_FOLDER']
    index = data['INDEX_DOWNLOAD']
    playlist = pytube.Playlist(url)

    # physically downloading the audio track
    if index == "True":
        i = 1
        for video in playlist.videos:
            video.streams.get_highest_resolution().download(output_path=folder, filename=f"[{i}] {video.title}")
            i += 1
    else:
        for video in playlist.videos:
            video.streams.get_highest_resolution().download(output_path=folder)


def download(mode=1, url=''):
    """Call playlist or video download"""
    # Video download
    if mode == 1:
        thread = Thread(target=download_video, args=(url,))
        thread.start()
    elif mode == 2:
        thread = Thread(target=download_playlist, args=(url,))
        thread.start()


def save_settings(color=BG_COLOR, folder=DOWNLOAD_FOLDER, index=INDEX_DOWNLOAD):
    """Save settings in a json files"""
    if color == "" or not is_valid_color(color):
        color = BG_COLOR
    if folder == "":
        folder = DOWNLOAD_FOLDER
    if index == "":
        index = INDEX_DOWNLOAD

    data = {
        "BACKGROUND_COLOR": color,
        "DOWNLOAD_FOLDER": folder,
        "INDEX_DOWNLOAD": index
    }
    with open("../Files/settings.json", "w") as f:
        json.dump(data, f, indent=5)


def get_settings():
    """Load settings from json file and return it"""
    with open("../Files/settings.json", "r") as f:
        data = json.load(f)
    return data


def set_check(chk):
    data = get_settings()
    index = data['INDEX_DOWNLOAD']
    index = "False" if index == "True" else "True"
    save_settings(index=index)
    chk.config(fg="green" if index == "True" else "red")
    chk.update()


def settings_window():
    """Display settings window"""
    data = get_settings()
    bg_color = data['BACKGROUND_COLOR']
    index = data['INDEX_DOWNLOAD']
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
    chk = tk.Checkbutton(window, text="Is index", command=lambda: set_check(chk), fg="green" if index == "True"
                         else "red")
    chk.pack(pady=20)

    function_button = tk.Button(window, text=title_label[2], width=20,
                                command=lambda: save_settings(user_entry_list[0].get(), user_entry_list[1].get()))
    function_button.pack(pady=20)

    window.mainloop()


def draw_component(window):
    """Display tkinter component on window"""
    data = get_settings()
    bg_color = data['BACKGROUND_COLOR']
    settings_button_image = tk.PhotoImage(file="../Images/gear.png").subsample(2)
    settings_button = tk.Button(window, image=settings_button_image, command=lambda: settings_window(),
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
                                    command=lambda button=i: download(button + 1, user_entry[button].get()))
        playlist_button.pack(pady=10)
