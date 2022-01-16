from __future__ import unicode_literals
import sys
import youtube_dl

ydl_opts = {'outtmpl': "in.mp4"
            ,'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]
            }

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([sys.argv[1]])
