import os
import subprocess
from typing import List

import yaml
import youtube_dl

import data_utils


def read_yaml(file_name : str):
    with open(file_name, "r", encoding='utf-8') as f:
        return yaml.safe_load(f)

def download_type(language_name: str, video_type: data_utils.Youtube_video_types, urls: List[str]):
    outtmpl = f"{data_utils.raw_folder_name}/{language_name}/{video_type.name}/"
    if video_type.value.folder_name:
        outtmpl += f"%({video_type.value.folder_name})s/" 
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl + "%(title)s.%(ext)s"
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
            download_type(language_name, type,
                          [f"{type.value.url}{id}" for id in video_types[type.name]])


if __name__ == '__main__':
    sources = read_yaml("sources.yml")
    for language_name, video_types in sources.items():
        download_language(language_name, video_types)
