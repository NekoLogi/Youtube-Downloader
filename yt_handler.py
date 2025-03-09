import os
import re
from pytubefix import YouTube
import subprocess


download_folder = ""
ext = ""
ffmpeg_path = ""


def init():
    global download_folder
    download_folder = ".\downloads"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    global ffmpeg_path
    if os.name=='nt':
        ffmpeg_path = "./ffmpeg-win/bin/ffmpeg.exe"
    else:
        ffmpeg_path = "./ffmpeg-linux/ffmpeg"

def sanitize_filename(filename):
    return re.sub(r'[\\\/:*?"<>|]', '_', filename).strip()

def download_audio(url:str, count=1):
    init()
    try:
        yt = YouTube(url)
        try:
            video_label = yt.title
        except Exception:
            video_label = url
        print(f"\nProcessing video: {video_label}")
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if not audio_stream:
            print(" - No audio stream found, skipping.")
            return
        global ext
        ext = audio_stream.mime_type.split('/')[-1]
        temp_filename = os.path.join(download_folder, f"temp_{count}.{ext}")
        print(f" - Downloading audio to {temp_filename}")
        audio_stream.download(output_path=download_folder, filename=f"temp_{count}.{ext}")
    except Exception as e:
        print(f"Error processing audio {count}: {e}")
    return yt

def download_video(url:str, count=1):
    init()
    try:
        yt = YouTube(url)
        try:
            video_label = yt.title
        except Exception:
            video_label = url
        print(f"\nProcessing video: {video_label}")
        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()
        
        if not video_stream:
            print(" - No video stream found, skipping.")
            return
        global ext
        ext = video_stream.mime_type.split('/')[-1]
        print(f" - Downloading video {video_label} ...")
        video_stream.download(output_path=download_folder, filename=f'temp_video.{ext}')
        audio_stream.download(output_path=download_folder, filename=f'temp_audio.{ext}')
    except Exception as e:
        print(f"Error processing video {count}: {e}")
    return yt


def convert_to_mp3(yt:YouTube, count=1, numeric_output=False):
    temp_filename = os.path.join(download_folder, f"temp_{count}.{ext}")
    output_filename = ""
    if numeric_output:
        output_filename = os.path.join(download_folder, f"{count}.mp3")
    else:
        output_filename = os.path.join(download_folder, f"{sanitize_filename(yt.title)}.mp3")

    command = [
        ffmpeg_path,
        "-y",
        "-i", temp_filename,
        "-b:a", "320k",
        output_filename
    ]
    print(" - Converting to MP3 with 320kbps...")
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    os.remove(temp_filename)
    print(f" - Finished: {output_filename}")

def merge_to_mp4(yt:YouTube, count=1, numeric_output=False):
    output_filename = ""
    if numeric_output:
        output_filename = os.path.join(download_folder, f"{count}.{ext}")
    else:
        output_filename = os.path.join(download_folder, f"{sanitize_filename(yt.title)}.{ext}")

    command = [
        ffmpeg_path,
        f"-i", os.path.join(download_folder, f"temp_video.{ext}"),
        f"-i", os.path.join(download_folder, f"temp_audio.{ext}"),
        "-c", "copy", output_filename
    ]
    print(f" - Merging {ext} files (Audio, Video) ...")
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    os.remove(os.path.join(download_folder, f"temp_video.{ext}"))
    os.remove(os.path.join(download_folder, f"temp_audio.{ext}"))
    print(f" - Finished: {output_filename}")
