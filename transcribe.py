# If you don't have pytube installed, then install it first using the following command: # pip install pytube
import sys
from time import process_time_ns
from pytube import Playlist
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

# this is the twiml AI podcast playlist - all episodes
TWIML_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLILZm3MRkvH83C46bZ4rPmB-jKWBltWkP"
MP3_PATH = "twiml-episodes"
TWIML_PLAYLIST_FILENAME = "twiml-playlist.txt"

# We use basic ANSI escape codes to color the output. These are all foreground colors.
class textColors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
    MAGENTA = '\x1b[35m'
    CYAN = '\x1b[36m'
    BLACK = '\x1b[30m'
    WHITE = '\x1b[37m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    UNDERLINE = '\033[4m' 


# from a youtube playlist, get all the video urls, titles, and episode numbers and save them to a text file
def savePlaylistToFile(playlist_url, playlist_filename):
    p = Playlist(playlist_url)
    with open(playlist_filename, 'w', encoding="utf8") as f:
        for index, url in enumerate(p.video_urls, start=1):
            yt = YouTube(url)
            print(index, '|' + yt.title + '|' + url )
            f.write(str(index) + '|' + yt.title + '|' + url + '\n')
        print("Playlist saved to file" + playlist_filename + " with " + str(index) + " episodes.")


# from a youtube playlist, get the video url, title, and save it as a mp3 file
def downloadVideoFromPlaylist(playlist_url, path):
    playlist = Playlist(playlist_url)
    for index, video in enumerate(playlist.videos, start=1):
        # if index < 286:
        #     continue
        print("Downloading #" + str(index) + " ... " + video.title)
        try:
            tempFileName = validFilename(str(index) + '_' + video.title + ".mp3")
            video.streams.filter(only_audio=True).first().download(output_path=MP3_PATH, filename=tempFileName)
        except IOError:
            print(f"{textColors.FAIL}Error: can\'t save the following file. Most likely it has an invalid character in the name.{textColors.RESET}")
            print("File: " + tempFileName)
        except VideoUnavailable:
            print("{textColors.FAIL}Video: " + tempFileName + " is unavailable, skipping.{textColors.RESET}")
    print("Download complete. Number of episodes downloaded: " + str(index))


# download mp3 from youtube video url
def downloadVideoFromURL(video_url, path):
    yt = YouTube(video_url)
    tempFileName = validFilename(yt.title + ".mp3")
    yt.streams.filter(only_audio=True).first().download(output_path=MP3_PATH, filename=tempFileName)
    print("File downloaded: " + tempFileName)


# check if a filename is valid
def is_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return all(c.isalnum() or c in "._-()" for c in s)


# convert a string to a valid filename
def validFilename(s):
    s = str(s).strip().replace(' ', '_')
    s = str(s).strip().replace('/', '-')
    s = str(s).strip().replace('&', 'and')
    s = str(s).strip().replace('\'', '')
    s = str(s).strip().replace('"', '')
    s = str(s).strip().replace(':', '-')
    s = str(s).strip().replace('*', '')
    return s


# Choose what we want to do:
print("What you want to do:")
print("1. For a given playlist, save the details of the episodes (metadata) to a file ")
print("2. Download and save as mp3 files, all the episode for a playlist")
print("3. Download a single episode and save as mp3 (for a given URL")
print("0. I changed my mind, I don't want to do anything")

try:
    choice = int(input(f"{textColors.MAGENTA}Enter your choice (1-3):{textColors.RESET} "))
except ValueError:
    print(f"{textColors.WARNING}That's not an integer! Exiting...{textColors.RESET}")
    sys.exit(1)

if choice == 0:
    print(f"{textColors.OK}No worries. Exiting.{textColors.RESET}")
    sys.exit(0)
elif choice == 1:
    print(f"\n\nSaving details of the following playlist: {textColors.OK}" + TWIML_PLAYLIST_URL + f"{textColors.RESET}\n to the file: {textColors.OK}" + TWIML_PLAYLIST_FILENAME + f"{textColors.RESET}")
    answer = input("Are you sure you want to do this? [default: n] (y/n):")
    if answer == 'y':
        savePlaylistToFile(TWIML_PLAYLIST_URL, TWIML_PLAYLIST_FILENAME)
    else:
        print("Skipping. Thanks for playing...")
        sys.exit(0)
elif choice == 2:
    print(f"\n\nDownloading all episodes from playlist: {textColors.OK}" + TWIML_PLAYLIST_URL + f"{textColors.RESET}\nand saving to this location: {textColors.OK}" + MP3_PATH + f"{textColors.RESET}")
    answer = input(f"{textColors.WARNING}This can take a *long* time, and a lot of *bandwidth*. Are you sure you want to do this? [default: n] (y/n): {textColors.RESET}")
    if answer == 'y':
        downloadVideoFromPlaylist(TWIML_PLAYLIST_URL, MP3_PATH)
    else:
        print("Skipping. Thanks for playing...")
        sys.exit(0)
elif choice == 3:
    print("\n\nEnter the URL of the episode you want to download:")
    url = input()
    print("Downloading episode from URL: " + url + "\nand saving to this location:" + MP3_PATH)
    downloadVideoFromURL(url, MP3_PATH)
else:
    print(f"{textColors.WARNING}Invalid choice. Exiting.{textColors.RESET}")
