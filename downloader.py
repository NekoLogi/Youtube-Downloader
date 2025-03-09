from pytubefix import Playlist
import yt_handler


def start_playlist(url, numeric=False):
    playlist = Playlist(url)
    video_urls = playlist.video_urls
    print(f"Found {len(video_urls)} videos in the playlist.")
    yt_data = None
    for count, video_url in enumerate(video_urls, start=1):
        yt_data = yt_handler.download_audio(video_url, count)
        if numeric:
            yt_handler.convert_to_mp3(None, count, True)
        else:
            yt_handler.convert_to_mp3(yt_data, count)

    print("\nAll downloads and conversions complete!")


def start_audio(url):
    yt_data = yt_handler.download_audio(url)
    yt_handler.convert_to_mp3(yt_data)

    print("\nAll downloads and conversions complete!")


def start_video(url):
    yt_data = yt_handler.download_video(url)
    if not yt_data:
        print("Failed to download video!")
        return
    yt_handler.merge_to_mp4(yt_data)
    print("\nAll downloads and conversions complete!")
