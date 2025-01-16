import yt_dlp

YDL_OPTS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'retries': 3
}

def yt_dlp_search(query, url=False):
    if not url:
        query = f"ytsearch:{query}"
    
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(query, download=False)

        if info is None or url:
            return info
        else:
            return info['entries'][0]
