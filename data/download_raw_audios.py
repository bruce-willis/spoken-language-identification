import os
import subprocess
from typing import List

import yaml
import youtube_dl

import data_utils


def read_yaml(file_name : str):
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


def download_type(language_name: str, video_type: str, urls: List[str]):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{data_utils.raw_folder_name}/{language_name}/{video_type}/%(title)s.%(ext)s"
        # 'postprocessors': [{
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'wav'
        # }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)


def download_language(language_name: str, video_types):
    for type in data_utils.Youtube_video_types:
        if type.name in video_types:
            download_type(language_name, type.name,
                          [f"{type.value.url}{id}" for id in video_types[type.name]])


if __name__ == '__main__':
    sources = read_yaml("sources.yml")
    for language_name, video_types in sources.items():
        download_language(language_name, video_types)
