from __future__ import unicode_literals
from requests import get
import youtube_dl

import cache_manager
import message_sender


def get_video(arg: str) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'cache/%(id)s.%(etx)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            get(arg) 
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            if cache_manager.is_in_cache(video['id']):
                return video
            else:
                message_sender.send_message('**Downloading . . .**')
                ydl.download(['https://www.youtube.com/watch?v=' + video['id']])
        else:
            video = ydl.extract_info(arg, download=False)
            if cache_manager.is_in_cache(video['id']):
                return video
            else:
                message_sender.send_message('**Downloading . . .**')
                ydl.download(['https://www.youtube.com/watch?v=' + video['id']])
    return video