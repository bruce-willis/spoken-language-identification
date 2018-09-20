# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import yaml
import subprocess
import os
import youtube_dl


def read_yaml(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        return yaml.safe_load(f)


def download(language, source, source_name, source_type):
    output_path = "{0}/{1}".format(language, source_name)
    if os.path.exists(output_path):
        print(
            "skipping {0} {1} because the target folder already exists".format(
                source_type, source_name))
    else:
        print("downloading {0} {1}".format(source_type, source_name))
        command = """youtube-dl -i --max-downloads 500 --extract-audio --audio-format mp3 {0} -o "{1}/{2}/%(title)s.%(ext)s" """.format(
            source, language, source_name)
        subprocess.call(command, shell=True)


def download_user(language, user):
    user_selector = "ytuser:%s" % user
    download(language, user_selector, user, "user")


def download_playlist(language, playlist_name, playlist_id):
    download(language, playlist_id, playlist_name, "playlist")


def download_playlist1(language_name, playlist_name, playlist_id):
    os.makedirs(os.path.join(language_name, playlist_name), exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{language_name}/{playlist_name}/%(title)s.%(ext)s"
        # 'postprocessors': [{
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'wav'
        # }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/playlist?list={playlist_id}"])


def download_language(language_name, video_types):
    # if "users" in video_types:
    #     for user in video_types["users"]:
    #         download_user(language, user)
    os.makedirs(language_name, exist_ok=True)
    if "playlists" in video_types:
        for playlist_name, playlist_id in video_types["playlists"].items():
            # download_playlist(language, playlist_name, playlist_id)
            download_playlist1(language_name, playlist_name, playlist_id)


if __name__ == '__main__':
    sources = read_yaml("sources.yml")
    for language_name, video_types in list(sources.items()):
        download_language(language_name, video_types)
