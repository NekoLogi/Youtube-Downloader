import os
import sys
import downloader
    

def start(url):
    if url == None or url == "":
        print("URL is empty or null")
        return
    
    new_url = ""
    if "&list=" in url:
        new_url = url.split("&")[1]
        new_url = new_url.strip("&list=")
        new_url = "https://www.youtube.com/playlist?list=" + new_url
        if input("Numeric output? (y or n): ") == "y":
            downloader.start_playlist(new_url, True)
        else:
            downloader.start_playlist(new_url)      
    elif "?list=" in url:
        if input("Numeric output? (y or n): ") == "y":
            downloader.start_playlist(url, True)
        else:
            downloader.start_playlist(url)
    elif "watch?v=" in url:
        format = input("Available formats:\n\t1 = Video\n\t2 = Audio\n\nEnter number: ")
        if  format == "1":
            downloader.start_video(url)
        else:
            downloader.start_audio(url)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

cls()
url = ""
try:
    url = sys.argv[1]
except Exception:
    pass
if url == "" or url == None:
    url = input("Enter URL: ")
start(url)