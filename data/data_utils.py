from enum import Enum
from typing import NamedTuple

""" 
Abstract youtube video type
:param str url: template url of type
:param str folder_name: output folder format for youtube_dl
"""
Type = NamedTuple("TypeInfo", [("url", str), ("folder_name", str)])

""" supported youtube video types """
class Youtube_video_types(Enum):
    playlists = Type("https://www.youtube.com/playlist?list=", "playlist_title")
    channels = Type("https://www.youtube.com/channel/", "uploader")
    users = Type("https://www.youtube.com/user/", "uploader")
    videos = Type("https://www.youtube.com/watch?v=", "")


raw_folder_name : str = "raw"